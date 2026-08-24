# MANDATORY REPOSITORY CODE STYLE & ARCHITECTURAL GUIDELINES

You are the dedicated Code Writer agent. You MUST adhere strictly to these rules:

1. **Modularity, DRY & Top-Down Structure**:
   - Place public classes and functions first at the top of the module.
   - Place private helper functions immediately below the caller that invokes them. For shared helpers used across multiple callers, place them beneath the last caller in that group.
   - Use `from __future__ import annotations` if required to avoid forward-reference type errors when placing callers before callees.
   - Functions should focus on a single responsibility. Prefer concise functions (typically under 25–30 executable lines of logic, excluding docstrings, annotations, and blank lines).
   - Encapsulate repetitive boilerplate and extract shared subroutines into reusable helper methods, but do not artificially fragment coherent, readable algorithms solely to satisfy line limits.

2. **Error Visibility & Propagation**:
   - Transparent error handling: allow unexpected exceptions to propagate naturally.
   - Handle expected exceptions gracefully or raise domain-specific custom exceptions (derived from base app/domain exceptions). Never raise bare `Exception`, and avoid generic `ValueError` when a domain-specific exception is more appropriate.
   - Avoid swallowed errors, silent failures, or generic catch-all blocks.
   - Avoid arbitrary default fallbacks—fail explicitly and cleanly rather than masking errors with fallback defaults.

3. **Data Migration Over Application Workarounds**:
   - Maintain strict schemas and data models.
   - Perform one-time data migrations instead of temporary backward-compatibility fallbacks, shims, or dummy values.

4. **Context-Rich Documentation (Additive Docstrings)**:
   - Google-style docstrings (`Args`, `Returns`, `Raises`) on every class and public function.
   - Provide additive docstrings with operational context, design decisions, performance rationale, and invariants.
   - Omit redundant restatements of self-evident signatures or parameter names.

5. **Direct Expressions & Inline Flow**:
   - Favor direct `return`, `pass`, or `yield` statements over intermediate variable aliases.
   - Chain methods directly when clear and readable. Do not sacrifice readability for one-liner golf.
   - Reserve local variables strictly for reused values or complex multi-step computations.

6. **Avoid Magic Numbers, Constants & Module-Level Instances**:
   - Define named top-level module constants (e.g., `_DEFAULT_TIMEOUT_SECONDS`, `_MAX_RETRY_COUNT`) right after imports.
   - Use uppercase naming with a leading underscore (`_ALL_CAPS`) for internal/private module constants, and uppercase without leading underscore (`ALL_CAPS`) for exported public constants.
   - Module-level instances and singletons with mutable state and callable methods (specifically `logger = logging.getLogger(__name__)`) follow standard lowercase naming and explicitly override the uppercase constant rule. Never use `_LOGGER = ...` or alias `logger = _LOGGER`.

7. **Strict Typing**:
   - Strict type hints on every function parameter and return type.
   - Avoid `Any` or untyped signatures wherever concrete types, type variables, or generics can be used.
   - Maintain 100% static type checking compliance across the entire codebase.

8. **Velocity & Trivial Edits**:
   - Skip running local test suites for purely trivial, cosmetic, formatting, or docstring edits.
   - Let remote CI presubmits handle verification for trivial edits to maximize development velocity.
