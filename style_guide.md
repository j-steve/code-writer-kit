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
   - Google-style docstrings (`Args`, `Returns`, `Raises`) on every class and public function.
   - Provide additive docstrings with operational context, design decisions, performance rationale, and invariants.
   - Omit redundant restatements of self-evident signatures or parameter names.

7. **Direct Expressions & Inline Flow**:
   - Favor direct `return`, `pass`, or `yield` statements over intermediate variable aliases.
   - Chain methods directly when clear and readable. Do not sacrifice readability for one-liner golf.
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

10. **No Local Test Suite Execution**:
    - NEVER execute local unit tests or test suites (`pytest`, `bazel test`, `npm test`, etc.).
    - Only run fast static checks (`ruff check`, `ruff format --check`, `pyright`) if needed for syntax and type validation.
    - Let remote CI presubmits handle test execution to maximize developer velocity and avoid unnecessary environment overhead.
