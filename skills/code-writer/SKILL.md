---
name: code-writer
description: Workflow and procedural guide for delegating code writing tasks to the dedicated code_writer subagent in compliance with code-writer-kit.
---

# Code Writer Delegation Workflow

When writing, creating, or modifying code files, always delegate the task to the dedicated `code_writer` subagent.

## Rules & Invariants
1. **Always use `code_writer`**: Never edit or create code directly in the parent agent.
2. **System Prompt Alignment**: Ensure the `code_writer` system prompt includes the contents of `style_guide.md`.
3. **No Local Test Suites**: `code_writer` must NEVER run local unit tests or test commands (`pytest`, `bazel test`). Only fast static linting/type-checking (`ruff`, `pyright`) is allowed if necessary. Remote CI presubmits handle test verification.
