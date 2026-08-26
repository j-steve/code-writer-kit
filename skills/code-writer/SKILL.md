---
name: code-writer
description: Workflow and procedural guide for delegating code writing tasks to the dedicated code_writer subagent in compliance with code-writer-kit.
---

# Code Writer Skill

This skill explains how to utilize the `code_writer` subagent to fulfill file write operations in projects governed by `code-writer-kit`.

## Workflow

1. **Read Guidelines**: Read `style_guide.md` to ensure full alignment with type hinting, docstring formatting, custom exceptions, and function modularity.
2. **Define Subagent**: Define `code_writer` with `enable_write_tools=True` and the style guide as `system_prompt` if not already defined:
   ```json
   {
     "name": "code_writer",
     "enable_write_tools": true,
     "system_prompt": "<contents of style_guide.md>"
   }
   ```
3. **Invoke Subagent**: Launch `code_writer` with a clear, concise instruction describing the target file and requirements:
   ```json
   {
     "TypeName": "code_writer",
     "Role": "Code Writer",
     "Prompt": "Implement feature X in file Y adhering to all style rules."
   }
   ```

## Rules & Invariants
1. **Always use `code_writer`**: Never edit or create code directly in the parent agent.
2. **System Prompt Alignment**: Ensure the `code_writer` system prompt includes the contents of `style_guide.md`.
3. **No Local Test Suites or Type Checkers**: `code_writer` must NEVER run local unit tests, test suites (`pytest`, `bazel test`), or local type checkers (`pyright`, `mypy`). Only fast formatting/linter checks (`ruff check`, `ruff format`) are allowed if necessary. Remote CI presubmits strictly handle full type checking and test verification.
