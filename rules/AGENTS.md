# Code Writer Kit Guardrails

- **Style Guide Enforcement**: The primary purpose of the `code_writer` subagent is to strictly enforce all repository code style, architectural, and quality standards.
- **Mandatory Delegation**: All modifications to code and documentation files (`.py`, `.md`) must be performed by the dedicated `code_writer` subagent via `invoke_subagent(TypeName="code_writer", ...)`.
- **Direct Modifications**: Non-code files (e.g. `.json`, `.yaml`, `.txt`, configs) and temporary files (in `scratch/` or `/tmp/`) may be created or edited directly.
- **Subagent Availability**: The `code_writer` subagent is pre-defined by the plugin. If not available in the active session, inspect `style_guide.md`, call `define_subagent` with the style guide as `system_prompt`, and invoke `code_writer`.
- **Targeted Verification**: The `code_writer` subagent may run fast static checks (`ruff`, `pyright`, `mypy`) and isolated, target-specific unit tests, but MUST NEVER execute full-repo monolithic test suites (e.g. `bazel test //...`) or heavy integration test suites locally. Full verification is handled by remote CI presubmits.
