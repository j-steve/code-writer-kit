---
name: python-style
description: Mandatory Python coding standards, top-down ordering, typing, docstrings, modularity, explicit parameter extraction, and targeted verification.
---

# MANDATORY REPOSITORY CODE STYLE & ARCHITECTURAL GUIDELINES

You are the dedicated Code Writer agent. You MUST adhere strictly to these rules:

1. **Top-Down Sequential Ordering (Caller Before Callee)**:
   - Place public classes and functions first at the top of the module.
   - Place private helper functions immediately below the caller that invokes them.
   - Place shared helper functions used across multiple callers beneath the last caller in that group.
   - Use `from __future__ import annotations` if required to avoid forward-reference type errors when placing callers before callees.

2. **Modularity & Single Responsibility**:
   - Functions and methods should focus strictly on a single responsibility.
   - Prefer concise functions (typically under 25–30 executable lines of logic, excluding docstrings, annotations, and blank lines).
   - Break complex, nested, or multi-step workflows into smaller, focused helper functions placed immediately below the caller.
   - Do not artificially fragment coherent, readable algorithms solely to satisfy line limits; maintain clean readability.
   - **Explicit Parameter Passing & Call-Site Extraction**: Child and helper functions should accept only the specific domain parameters, primitives, or narrow objects they need to operate—do not pass monolithic configuration or global context objects (e.g., `cfg`, `context`) down into leaf helpers. Extract nested attributes or execute retrieval methods directly inline at the call site without creating single-use temporary variables.
     - *Anti-pattern 1 (Monolithic Passthrough)*: Parent calls `_fetch_data(cfg)` and `_fetch_data` reaches into `cfg.auth.get_token()`.
     - *Anti-pattern 2 (Single-Use Variable Alias)*: Parent does `token = cfg.auth.get_token()` followed by `_fetch_data(token=token)`.
     - *Preferred (Inline Call-Site Extraction)*: Parent calls `_fetch_data(token=cfg.auth.get_token())`, keeping `_fetch_data(token: str)` completely decoupled and trivially testable.

3. **Don't Repeat Yourself (DRY) & Cross-Module Sharing**:
   - Never duplicate logic, data definitions, or configuration across files or functions.
   - If a constant, identifier, template name, schema, or logic snippet is referenced in multiple modules (such as prompt names, shared graph node IDs, or domain models), move it to a single authoritative shared file (e.g., `src/prompts/constants.py`, `src/graphs/common.py`) and import it.
   - Encapsulate upstream boilerplate, data transformations, and repeated subroutines into reusable helper methods or domain services.

4. **Error Visibility & Propagation**:
   - Transparent error handling: allow unexpected exceptions to propagate naturally.
   - Handle expected exceptions gracefully or raise domain-specific custom exceptions (derived from base app/domain exceptions). Never raise bare `Exception`, and avoid generic `ValueError` when a domain-specific exception is more appropriate.
   - Avoid swallowed errors, silent failures, or generic catch-all blocks.
   - Avoid arbitrary default fallbacks—fail explicitly and cleanly rather than masking errors with fallback defaults.

5. **Data Migration Over Application Workarounds**:
   - Maintain strict schemas and data models.
   - Perform one-time data migrations instead of temporary backward-compatibility fallbacks, shims, or dummy values.

6. **Context-Rich Documentation (Additive Docstrings)**:
   - Google-style docstrings on public classes and public functions.  You should also document `Args`, `Returns`, and `Raises` if it aids readability (i.e., if isn't already self-explanatory or obvious from the basic docstring), 
   - Provide additive docstrings with operational context, design decisions, performance rationale, and invariants.
   - Omit redundant restatements of self-evident signatures or parameter names.

7. **Direct Expressions & Inline Flow**:
   - Favor direct `return`, `pass`, or `yield` statements over intermediate variable aliases.
   - Chain methods directly when clear and readable. Do not sacrifice readability for one-liner golf.
   - Prohibit trivial variable reassignments and single-use intermediate variable aliases for object, config, or model attributes (such as `user_id = cfg.user_id`, `state_messages = state['messages']`, etc.).
   - Access attributes and fields directly from the validated model, configuration object, or state mapping (e.g., `cfg.user_id`, `cfg.comm_origin`) rather than creating redundant local variable aliases.
   - Reserve local variables strictly for reused values or complex multi-step computations.

8. **Avoid Magic Numbers, Constants & Structured Enums**:
   - Define named top-level module constants (e.g., `_DEFAULT_TIMEOUT_SECONDS`, `_MAX_RETRY_COUNT`) right after imports.
   - Use uppercase naming with a leading underscore (`_ALL_CAPS`) for internal/private module constants, and uppercase without leading underscore (`ALL_CAPS`) for exported public constants.
   - Group related string constants into typed structures (e.g., `class NodeName(StrEnum): ...`, `class PromptName(StrEnum): ...`) rather than maintaining fragmented loose string constants.
   - Module-level instances and singletons with mutable state and callable methods (specifically `logger = logging.getLogger(__name__)`) follow standard lowercase naming and explicitly override the uppercase constant rule. Never use `_LOGGER = ...` or alias `logger = _LOGGER`.

9. **Strict Typing**:
   - Strict type hints on every function parameter and return type.
   - Avoid `Any` or untyped signatures wherever concrete types, type variables, or generics can be used.
   - Maintain 100% static type checking compliance across the entire codebase.

10. **Targeted Verification vs. Monolithic Test Suites**:
    - Fast static checks (`ruff check`, `ruff format`, `pyright`, `mypy`) and isolated, target-specific unit tests (e.g., testing a single target or file) are permitted and encouraged to catch regressions and type mismatches before handoff.
    - NEVER run full-repo monolithic test suites (e.g. `bazel test //...`) or heavy end-to-end integration suites locally; remote CI presubmits handle full regression testing.
