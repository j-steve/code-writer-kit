# Code Writer Kit Guardrails

- All modifications to code and documentation files (`.py`, `.md`) must be performed by the dedicated `code_writer` subagent to enforce repository style and quality standards.
- Non-code files (e.g. `.json`, `.yaml`, `.txt`, configs) and temporary files (in `scratch/` or `/tmp/`) may be created or edited directly.
- When delegating to `code_writer`, inspect `style_guide.md`, call `define_subagent` with the style guide as `system_prompt`, and invoke `code_writer`.
- The `code_writer` subagent may run fast static checks (`ruff`, `pyright`, `mypy`) and isolated, target-specific unit tests, but MUST NEVER execute full-repo monolithic test suites (e.g. `bazel test //...`) or heavy integration test suites locally. Full verification is handled by remote CI presubmits.
