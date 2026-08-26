---
name: code-writer
description: Workflow and procedural guide for delegating code writing tasks to the dedicated code_writer subagent in compliance with code-writer-kit.
---

# Code Writer Delegation Workflow

When writing, creating, or modifying code files, always delegate the task to the dedicated `code_writer` subagent.

## Rules & Invariants
1. **Always use `code_writer`**: Never edit or create code directly in the parent agent.
2. **System Prompt Alignment**: Ensure the `code_writer` system prompt includes the contents of `style_guide.md`.
3. **No Local Test Suites or Type Checkers**: `code_writer` must NEVER run local unit tests, test suites (`pytest`, `bazel test`), or local type checkers (`pyright`, `mypy`). Only fast formatting/linter checks (`ruff check`, `ruff format`) are allowed if necessary. Remote CI presubmits strictly handle full type checking and test verification.
