#!/usr/bin/env python3
"""Daily mechanical audit of the upstream repo for PR candidates.

Runs the checks the upstream's CONTRIBUTING.md declares as maintainer
priorities and emits a markdown report to stdout. Each finding is a
*candidate* — the agent running the loop must still dedup it against
existing issues/PRs before implementing anything.

Repo-specific checks (Windows footguns script, skills HARDLINE standard,
installer drift) degrade gracefully to a skip line when the target repo
does not have the corresponding files, so this script is safe to point at
any repository.

Usage:
    python audit.py [path-to-upstream-clone]   # default: cwd
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
EXCLUDED_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__", "build",
    "dist", ".tox", ".mypy_cache", ".pytest_cache", "site-packages",
}
MAX_LINES_PER_SECTION = 120


def walk_py(root: Path):
    for path in root.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def section(title: str, lines: list[str]) -> None:
    print(f"\n## {title}\n")
    if not lines:
        print("No findings.")
        return
    shown = lines[:MAX_LINES_PER_SECTION]
    for line in shown:
        print(line)
    if len(lines) > len(shown):
        print(f"... (+{len(lines) - len(shown)} lines omitted)")


def run_footguns() -> list[str]:
    """scripts/check-windows-footguns.py --all (full-tree audit), if present."""
    script = REPO / "scripts" / "check-windows-footguns.py"
    if not script.exists():
        return ["SKIP: scripts/check-windows-footguns.py not present in this repo"]
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--all"],
            cwd=REPO, capture_output=True, text=True, timeout=600,
            encoding="utf-8", errors="replace",
        )
    except subprocess.TimeoutExpired:
        return ["ERROR: timeout running check-windows-footguns.py"]
    out = (r.stdout + "\n" + r.stderr).strip()
    if r.returncode == 0:
        return []
    return [f"exit={r.returncode}"] + out.splitlines()


def scan_os_kill_zero() -> list[str]:
    """os.kill(pid, 0) outside tests/ — presumed silent-kill bug on Windows."""
    pattern = re.compile(r"os\.kill\(\s*[^,)]+,\s*0\s*\)")
    suppress = re.compile(r"#\s*windows-footgun\s*:\s*ok", re.IGNORECASE)
    hits = []
    for path in walk_py(REPO):
        rel = path.relative_to(REPO)
        if rel.parts and rel.parts[0] in ("tests", "scripts"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            # Code part only: ignore mentions in comments and in RST
            # literals (``...``) inside docstrings.
            code = line.split("#", 1)[0]
            if "``" in code:
                continue
            if pattern.search(code) and not suppress.search(line):
                hits.append(f"- `{rel.as_posix()}:{i}` — `{line.strip()}`")
    return hits


def scan_unbounded_deps() -> list[str]:
    """PyPI deps with >=X and no <next_major ceiling (supply-chain policy)."""
    pyproject = REPO / "pyproject.toml"
    if not pyproject.exists():
        return ["SKIP: pyproject.toml not present in this repo"]
    hits = []
    dep_re = re.compile(r'"([A-Za-z0-9_.\[\]-]+)\s*(>=[^"]*)"')
    for i, line in enumerate(
        pyproject.read_text(encoding="utf-8", errors="replace").splitlines(), 1
    ):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for m in dep_re.finditer(line):
            name, spec = m.group(1), m.group(2)
            if "<" not in spec and "==" not in spec:
                hits.append(
                    f"- `pyproject.toml:{i}` — `{name}{spec}` has no version ceiling"
                )
    return hits


def _frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return m.group(1) if m else ""


def scan_skills() -> list[str]:
    """Skills violating the HARDLINE standard: description > 60 chars; POSIX-only code without a platforms gate."""
    posix_markers = [
        ("import fcntl", "fcntl"),
        ("import termios", "termios"),
        ("os.setsid", "os.setsid"),
        ("os.killpg", "os.killpg"),
        ("signal.SIGKILL", "SIGKILL"),
        ("/proc/", "/proc"),
        ("osascript", "osascript"),
    ]
    hits = []
    any_root = False
    for base in ("skills", "optional-skills"):
        root = REPO / base
        if not root.exists():
            continue
        any_root = True
        for skill_md in sorted(root.rglob("SKILL.md")):
            rel = skill_md.relative_to(REPO)
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            fm = _frontmatter(text)

            desc = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
            if desc:
                d = desc.group(1).strip().strip('"').strip("'")
                if len(d) > 60:
                    hits.append(
                        f"- `{rel.as_posix()}` — description is {len(d)} chars (max 60)"
                    )

            has_platforms = bool(re.search(r"^platforms:", fm, re.MULTILINE))
            if not has_platforms:
                skill_dir = skill_md.parent
                found: set[str] = set()
                for script in skill_dir.rglob("*"):
                    if script.suffix not in (".py", ".sh") or not script.is_file():
                        continue
                    try:
                        body = script.read_text(encoding="utf-8", errors="replace")
                    except OSError:
                        continue
                    for marker, label in posix_markers:
                        if marker in body:
                            found.add(label)
                if found:
                    hits.append(
                        f"- `{rel.as_posix()}` — uses {sorted(found)} without `platforms:` in frontmatter"
                    )
    if not any_root:
        return ["SKIP: no skills/ or optional-skills/ directory in this repo"]
    return hits


def scan_installer_drift() -> list[str]:
    """Latest commits touching install.sh vs install.ps1 — investigate drift."""
    targets = [
        n for n in ("scripts/install.sh", "scripts/install.ps1")
        if (REPO / n).exists()
    ]
    if len(targets) < 2:
        return ["SKIP: repo does not ship paired install.sh/install.ps1"]
    lines = []
    for name in targets:
        try:
            r = subprocess.run(
                ["git", "log", "-3", "--format=%h %ad %s", "--date=short", "--", name],
                cwd=REPO, capture_output=True, text=True, timeout=60,
                encoding="utf-8", errors="replace",
            )
            lines.append(f"### {name}")
            lines.extend(f"- {l}" for l in r.stdout.strip().splitlines())
        except (OSError, subprocess.TimeoutExpired) as exc:
            lines.append(f"### {name} — ERROR: {exc}")
    lines.append(
        "> If one received fixes the other didn't, drift is likely — "
        "compare the diffs of the commits above."
    )
    return lines


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    head = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()
    print(f"# Mechanical audit @ {head}")
    print(f"Repo: {REPO}")

    section("1. Windows footguns (scripts/check-windows-footguns.py --all)", run_footguns())
    section("2. os.kill(pid, 0) outside tests/ (silent-kill on Windows)", scan_os_kill_zero())
    section("3. Dependencies without version ceilings (supply chain)", scan_unbounded_deps())
    section("4. Skills violating the HARDLINE standard", scan_skills())
    section("5. install.sh vs install.ps1 drift", scan_installer_drift())

    print("\n---")
    print(
        "Reminder: every finding is a CANDIDATE. Dedup is mandatory "
        "(gh search prs/issues) before implementing anything."
    )


if __name__ == "__main__":
    main()
