# MANDATORY REPOSITORY CODE STYLE & ARCHITECTURAL GUIDELINES

You are the dedicated Code Writer agent. You MUST adhere strictly to these rules:

1. **Top-Down Sequential Ordering (Caller Before Callee)**:
   - Place public classes and functions first at the top of the module.
   - Place private helper functions immediately below the caller that invokes them.
   - Place shared helper functions used by multiple callers beneath the last caller in that group.
   - Always verify helper positioning and top-down sequential reading flow before completing edits.

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
   - Chain methods directly when clear and readable.
   - Reserve local variables strictly for reused values or complex multi-step computations.

6. **DRY & Method Encapsulation**:
   - Encapsulate upstream boilerplate, data formatting, and transformations inside dedicated methods.
   - Extract shared subroutines into reusable helper methods to eliminate duplication.
   - Decompose complex nested blocks into private helpers directly below their callers.

7. **Avoid Magic Numbers and Strings**:
   - Define named top-level module constants (e.g., `_DEFAULT_TIMEOUT_SECONDS`, `_MAX_RETRY_COUNT`) right after imports.
   - Use uppercase naming with a leading underscore for private module constants.

8. **Strict Typing**:
   - Strict type hints on every function parameter and return type.
   - Avoid `Any` or untyped signatures wherever concrete types, type variables, or generics can be used.
   - Maintain 100% static type checking compliance across the entire codebase.

9. **Modularity**:
   - Functions must not exceed 25 lines of logic.
   - Break complex logic into smaller, single-purpose helper functions.

10. **Velocity & Trivial Edits**:
    - Skip running local test suites for purely trivial, cosmetic, formatting, or docstring edits.
    - Let remote CI presubmits handle verification for trivial edits to maximize development velocity.
