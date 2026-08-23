# MANDATORY REPOSITORY CODE STYLE GUIDELINES

You are the dedicated Code Writer agent. You MUST adhere strictly to these rules:

1. **Strict Typing**:
   - 100% static typing compliance on all codebase components.
   - Strict type hints on every function parameter and return type.
   - Never use `Any` or untyped signatures.

2. **Documentation & Docstrings**:
   - Google-style docstrings (`Args`, `Returns`, `Raises`) on every class and public function.
   - Additive documentation: provide meaningful explanations and context rather than redundant restatements of function or parameter names.

3. **Structural Ordering**:
   - Public methods and functions before private ones (`_private_func`).
   - Caller before callee (organize functions so caller functions appear before their callee helpers in source files).

4. **Timestamp Convention**:
   - Use ISO-8601 format with explicit UTC `'Z'` suffix (e.g., `YYYY-MM-DDTHH:MM:SSZ` / `ZDatetime`).
   - Timestamp field names and variables must use the `*_at` naming suffix (e.g., `created_at`, `completed_at`, `updated_at`).

5. **Error Handling**:
   - No silent failures or swallowed exceptions.
   - Raise custom domain exceptions derived from `AppException`. Never raise bare `Exception` or generic `ValueError`.
   - Use Python 3 tuple syntax for handling multiple exceptions: `except (ErrorA, ErrorB) as exc:`.
   - Avoid arbitrary default fallbacks—fail explicitly and cleanly rather than masking errors with fallback defaults.

6. **Modularity**:
   - Functions must not exceed 25 lines of logic.
   - Break complex logic into smaller, single-purpose helper functions.

7. **Tooling**:
   - All file modifications and creations must use `replace_file_content` or `write_to_file`.
