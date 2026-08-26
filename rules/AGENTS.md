# Code Writer Kit Guardrails

- All code modifications (file creations, edits, refactors) must be performed by the dedicated `code_writer` subagent to enforce repository style and quality standards.
- When an agent needs to write or modify code files, it must:
  1. Inspect the style guide at `style_guide.md` (or the plugin's bundled style guide).
  2. Call `define_subagent` with `name="code_writer"`, `enable_write_tools=True`, and `system_prompt` matching the style guide.
  3. Call `invoke_subagent(TypeName="code_writer", ...)` with the specific task.
- The `code_writer` subagent MUST NEVER execute local unit tests, test suites (`pytest`, `bazel test`), or local type checkers (`pyright`, `mypy`). Verification is strictly handled by remote CI presubmits.
