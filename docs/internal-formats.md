# Internal format policy

The repository owns committed profiles, logs and anti-duplicate state, but it
must not invent a serialization contract separate from simplicio-runtime and
simplicio-loop.

The policy is recorded in config/json-boundaries.toml. The scanner
scripts/check_internal_formats.py runs in baseline mode while the upstream
HBP/HBI contracts are implemented:

- HBP is the target for append-only receipts and auditable contribution events.
- HBI is the target for indexed snapshots after Runtime HBI v1 conformance exists.
- TOML is used for human-authored policy/configuration.
- JSON is not an internal OSS-loop persistence, cache, IPC or evidence format.
- External/toolchain JSON is allowed only with an exact, owned inventory entry.

Baseline mode fails on unclassified findings and reports classified internal
findings as migration work. Strict mode also fails until the linked migration
issues are complete. The scanner prints Markdown so evidence can be persisted
through HBP rather than generating a new JSON report.

Related work:

- Runtime architecture: https://github.com/wesleysimplicio/simplicio-runtime/issues/3492
- OSS migration: https://github.com/wesleysimplicio/simplicio-loop-oss/issues/18
- OSS quality gate: https://github.com/wesleysimplicio/simplicio-loop-oss/issues/19
