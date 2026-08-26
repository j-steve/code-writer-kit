---
name: code-style
description: Mandatory baseline code style and architectural invariants for all code modifications: modularity, explicit parameter extraction, DRY, error visibility, direct expressions, and targeted verification.
---

# MANDATORY BASELINE CODE STYLE & ARCHITECTURAL INVARIANTS

You are the dedicated Code Writer agent. You MUST adhere strictly to these baseline rules for all code and architectural modifications across any programming language:

1. **Modularity & Single Responsibility**:
   - Functions, methods, and classes should focus strictly on a single, well-defined responsibility.
   - Prefer concise functions (typically under 25–30 executable lines of logic, excluding docstrings, annotations, and blank lines).
   - Break complex, nested, or multi-step workflows into smaller, focused helper routines placed logically near the caller.
   - Do not artificially fragment coherent, readable algorithms solely to satisfy line limits; maintain clean readability.
   - **Explicit Parameter Passing & Call-Site Extraction**: Child and helper functions should accept only the specific domain parameters, primitives, or narrow objects they need to operate—do not pass monolithic configuration or global context objects (e.g., `cfg`, `context`, `state`) down into leaf helpers. Extract nested attributes or execute retrieval methods directly inline at the call site without creating single-use temporary variables.
     - *Anti-pattern 1 (Monolithic Passthrough)*: Parent calls `fetch_data(cfg)` and `fetch_data` reaches deep into `cfg.auth.get_token()`.
     - *Anti-pattern 2 (Single-Use Variable Alias)*: Parent assigns `token = cfg.auth.get_token()` followed by `fetch_data(token=token)`.
     - *Preferred (Inline Call-Site Extraction)*: Parent calls `fetch_data(token=cfg.auth.get_token())`, keeping `fetch_data(token: str)` completely decoupled, focused, and trivially testable.

2. **Don't Repeat Yourself (DRY) & Single Source of Truth**:
   - Never duplicate logic, schemas, data definitions, or configuration across files or functions.
   - If a constant, identifier, template name, schema, or logic snippet is referenced across multiple modules or components, move it to a single authoritative shared module/file and import or reference it.
   - Encapsulate upstream boilerplate, data transformations, and repeated subroutines into reusable helper methods or domain services.

3. **Error Visibility & Propagation**:
   - Transparent error handling: allow unexpected exceptions or errors to propagate naturally.
   - Handle expected exceptions gracefully or raise domain-specific custom exceptions (derived from base application/domain exceptions). Never raise bare/generic base exceptions (e.g., bare `Exception`), and avoid generic error types (e.g., generic `ValueError`) when a domain-specific exception is more appropriate.
   - Avoid swallowed errors, silent failures, empty catch blocks, or generic catch-all blocks.
   - Avoid arbitrary default fallbacks—fail explicitly and cleanly rather than masking errors with fallback defaults.

4. **Data Migration Over Application Workarounds**:
   - Maintain strict schemas and data models.
   - Perform one-time data migrations instead of introducing temporary backward-compatibility fallbacks, shims, or dummy values.

5. **Direct Expressions & Inline Flow**:
   - Favor direct `return`, `pass`, or `yield` statements over intermediate variable aliases.
   - Chain methods directly when clear and readable. Do not sacrifice readability for one-liner golf.
   - Prohibit trivial variable reassignments and single-use intermediate variable aliases for object, config, or model attributes (such as `user_id = cfg.user_id`, `state_messages = state['messages']`, etc.).
   - Access attributes and fields directly from the validated model, configuration object, or state mapping rather than creating redundant local variable aliases.
   - Reserve local variables strictly for reused values or complex multi-step computations.

6. **Avoid Magic Numbers & Hardcoded Constants**:
   - Define named top-level constants rather than scattering hardcoded magic numbers or raw strings across business logic.
   - Group related constants logically into structured enumerations, constant mappings, or typed collections rather than maintaining loose, fragmented constants.

7. **Targeted Verification vs. Monolithic Test Suites**:
   - Fast static checks (linters, type checkers, formatters) and isolated, target-specific unit tests (e.g., testing a single target or file) are permitted and encouraged to catch regressions and type mismatches before handoff.
   - NEVER run full-repo monolithic test suites (e.g. `bazel test //...` or full repository test runners) or heavy end-to-end integration suites locally; remote CI presubmits handle full regression testing.
