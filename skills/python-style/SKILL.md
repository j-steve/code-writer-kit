---
name: python-style
description: Mandatory Python coding standards: top-down ordering, strict typing, Google docstrings, logger and constant conventions, and fast static verification.
---

# MANDATORY PYTHON CODE STYLE GUIDELINES

You are the dedicated Code Writer agent. In addition to the baseline `code-style` skill, you MUST adhere strictly to these Python-specific standards:

1. **Top-Down Sequential Ordering (Caller Before Callee)**:
   - Place public classes and functions first at the top of the module.
   - Place private helper functions immediately below the caller that invokes them.
   - Place shared helper functions used across multiple callers beneath the last caller in that group.
   - Always use `from __future__ import annotations` at the top of Python modules to avoid forward-reference type errors when placing callers before callees.

2. **Strict Typing**:
   - Strict type hints on every function parameter and return type.
   - Avoid `Any` or untyped signatures wherever concrete types, type variables, or generics can be used.
   - Maintain 100% static type checking compliance across the entire codebase.

3. **Context-Rich Google Docstrings (Additive Documentation)**:
   - Google-style docstrings on public classes and public functions.
   - Explicitly document `Args`, `Returns`, and `Raises` whenever it aids readability and adds non-trivial context (exceptions raised, operational context, constraints).
   - Provide additive docstrings with operational context, design decisions, performance rationale, and invariants.
   - Omit redundant restatements of self-evident signatures or parameter names.

4. **Logger & Constant Naming Conventions**:
   - Define named top-level module constants right after imports.
   - Use uppercase naming with a leading underscore (`_ALL_CAPS`) for internal/private module constants, and uppercase without leading underscore (`ALL_CAPS`) for exported public constants.
   - Group related string constants into typed structures (e.g., `class NodeName(StrEnum): ...`, `class PromptName(StrEnum): ...`) rather than maintaining fragmented loose string constants.
   - Module-level instances and singletons with mutable state and callable methods (specifically `logger = logging.getLogger(__name__)`) follow standard lowercase naming and explicitly override the uppercase constant rule. Never use `_LOGGER = ...` or alias `logger = _LOGGER`.

5. **Fast Static Verification**:
   - Fast static checks (`ruff check`, `ruff format`, `pyright`, `mypy`) and isolated, target-specific unit tests (e.g., testing a single target or file) are permitted and encouraged to catch regressions and type mismatches before handoff.
   - NEVER run full-repo monolithic test suites (e.g. `bazel test //...`) or heavy end-to-end integration suites locally; remote CI presubmits handle full regression testing.
