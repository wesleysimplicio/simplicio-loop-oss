#!/usr/bin/env python3
"""Check Simplicio-owned internal JSON paths without creating a JSON report.

The baseline mode classifies current findings and exits non-zero only for
unclassified paths. Strict mode (SIMPLICIO_FORMAT_STRICT=1 or --strict)
also fails for classified internal JSON until its migration issue is complete.
Output is Markdown on stdout; callers may persist the evidence through HBP.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "json-boundaries.toml"
SKIP = {".git", "work", "node_modules", "__pycache__", ".venv", "dist", "build"}
JSON_SUFFIXES = {".json", ".jsonl", ".ndjson"}
ALLOWED = {"toolchain_mandated", "external_output_contract", "third_party_protocol_boundary", "historical_documentation", "runtime_workspace", "policy_scanner"}
INTERNAL = {"internal_persistence", "internal_cache", "internal_ipc", "internal_fixture_or_evidence", "internal_index"}
SOURCE_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".tsx", ".rs", ".sh", ".ps1"}

def parse_policy() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    if not POLICY.exists():
        return entries
    for raw in POLICY.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line == "[[paths]]":
            if current:
                entries.append(current)
            current = {}
            continue
        if current is None or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        current[key] = value.strip().strip('"')
    if current:
        entries.append(current)
    return entries

def match(path: str, entries: list[dict[str, str]]) -> dict[str, str] | None:
    for entry in entries:
        pattern = entry.get("pattern", "")
        if pattern.endswith("/**") and path.startswith(pattern[:-2]):
            return entry
        if path == pattern:
            return entry
    return None

def files() -> list[Path]:
    found: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP for part in path.parts):
            continue
        if path.suffix.lower() in JSON_SUFFIXES:
            found.append(path)
    return found

def source_hits() -> list[tuple[Path, int, str]]:
    patterns = (
        re.compile(r"(^|\\s)(import|from)\\s+json\\b"),
        re.compile(r"serde_json|JSON\\.parse\\s*\\(|JSON\\.stringify\\s*\\("),
        re.compile(r"\\.jsonl\\b|\\.ndjson\\b"),
    )
    hits: list[tuple[Path, int, str]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        if any(part in SKIP for part in path.parts) or path == Path(__file__):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if any(pattern.search(line) for pattern in patterns):
                hits.append((path, number, line.strip()))
    return hits

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    strict = args.strict or os.environ.get("SIMPLICIO_FORMAT_STRICT") == "1"
    entries = parse_policy()
    unknown: list[str] = []
    migration: list[str] = []
    allowed: list[str] = []
    for path in files():
        rel = path.relative_to(ROOT).as_posix()
        entry = match(rel, entries)
        if entry is None:
            unknown.append(rel)
        elif entry.get("category") in INTERNAL:
            migration.append(f"{rel} ({entry.get('target_format', 'unassigned')})")
        else:
            allowed.append(f"{rel} ({entry.get('category', 'unknown')})")
    for path, line, text in source_hits():
        rel = path.relative_to(ROOT).as_posix()
        entry = match(rel, entries)
        if entry is None:
            unknown.append(f"{rel}:{line} — {text}")
        elif entry.get("category") in INTERNAL:
            migration.append(f"{rel}:{line} — {text}")
        else:
            allowed.append(f"{rel}:{line} ({entry.get('category', 'unknown')})")
    print("# Simplicio internal-format policy")
    print(f"\\nMode: {'strict' if strict else 'baseline'}")
    print("\\n## Allowed or explicitly bounded")
    print("\\n".join(f"- {item}" for item in sorted(set(allowed))) or "- none")
    print("\\n## Migration required")
    print("\\n".join(f"- {item}" for item in sorted(set(migration))) or "- none")
    print("\\n## Unclassified")
    print("\\n".join(f"- {item}" for item in sorted(set(unknown))) or "- none")
    if unknown:
        return 1
    if strict and migration:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
