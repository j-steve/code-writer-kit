# Code Writer Kit Guardrails

- **Style Guide Enforcement**: The primary purpose of the `code_writer` subagent is to strictly enforce all repository code style, architectural, and quality standards organized as modular skills (e.g., `skills/python-style/SKILL.md`).
- **Mandatory Delegation**: All modifications to code and documentation files (`.py`, `.md`) must be performed by the dedicated `code_writer` subagent via `invoke_subagent(TypeName="code_writer", ...)`.
- **Direct Modifications**: Non-code files (e.g. `.json`, `.yaml`, `.txt`, configs) and temporary files (in `scratch/` or `/tmp/`) may be created or edited directly.
- **Targeted Verification**: The `code_writer` subagent may run fast static checks (`ruff`, `pyright`, `mypy`) and isolated, target-specific unit tests, but MUST NEVER execute full-repo monolithic test suites (e.g. `bazel test //...`) or heavy integration test suites locally. Full verification is handled by remote CI presubmits.
