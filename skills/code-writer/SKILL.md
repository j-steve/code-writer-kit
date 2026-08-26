---
name: code-writer
description: Detailed procedural guide and runbook for delegating code and documentation modifications to the dedicated code_writer subagent.
---

# Code Writer Skill Runbook

This skill defines the complete operational procedure for delegating repository modifications to the dedicated `code_writer` subagent in environments managed by `code-writer-kit`. The primary responsibility of `code_writer` is rigorous enforcement of `style_guide.md`.

## 1. Scope & Guardrails

- **Style Guide Enforcement**: The core purpose of the `code_writer` subagent is strict adherence to repository architectural guidelines, top-down caller-before-callee ordering, modularity, explicit parameter passing, additive docstrings, and type safety standards.
- **Protected Targets**: All modifications (creations, edits, deletions, and refactors) targeting code or documentation files (specifically `.py` and `.md` extensions) must be executed by the `code_writer` subagent.
- **Unprotected / Exempt Targets**: Direct writes by the root agent are permitted for non-code files (e.g., `.json`, `.yaml`, `.toml`, `.txt`, configuration manifests) and temporary workspace paths (e.g., paths matching `/scratch/`, `/tmp/`, or `.system_generated`).
- **Hook Enforcement**: The PreToolUse hook (`scripts/enforce_writer.py`) intercepts unauthorized file operations on protected targets and returns a hard block instructing delegation.

## 2. Step-by-Step Delegation Procedure

### Step 1: Inspect Style & Architectural Guidelines
Read the base plugin `style_guide.md` and check for any workspace root `style_guide.md` augmentations to review the exact architectural requirements, coding conventions, type annotation rules, and docstring formats that `code_writer` will enforce.

### Step 2: Invoke the `code_writer` Subagent
The `code_writer` subagent is pre-defined by the plugin and can be invoked directly. Dispatch the subagent using `invoke_subagent` with a detailed prompt including target files, operational requirements, behavioral constraints, and verification instructions:

```json
{
  "TypeName": "code_writer",
  "Role": "Code Writer",
  "Prompt": "Implement feature X in src/feature.py according to style guidelines. Ensure caller-before-callee order, strict type annotations, and Google-style docstrings."
}
```

### Step 3: Fallback Subagent Definition (If Unmounted)
If the pre-defined `code_writer` subagent is not available in the active session, register it manually by reading `style_guide.md` and invoking `define_subagent`:

```json
{
  "name": "code_writer",
  "enable_write_tools": true,
  "system_prompt": "<contents of style_guide.md>"
}
```

Once defined, invoke `code_writer` as shown in Step 2.

### Step 4: Validate Subagent Deliverables
Review the completion report and file modifications returned by the subagent via `send_message`. Verify that all changes strictly adhere to `style_guide.md`.

## 3. Operational Invariants

1. **Mandatory Subagent Delegation**: Never bypass `code_writer` when authoring or editing protected `.py` or `.md` files.
2. **Style Guide Enforcement**: The `code_writer` subagent is strictly bounded by the rules in `style_guide.md`.
3. **Subagent Availability**: The `code_writer` subagent is pre-defined in the plugin. If unmounted, use `define_subagent` with `style_guide.md` as the system prompt.
4. **Verification Policy**:
   - The `code_writer` subagent may execute fast static checks (`ruff check`, `ruff format --check`, `pyright`, `mypy`) and isolated, target-specific unit tests to validate syntax and behavior.
   - The subagent MUST NEVER execute full-repo monolithic test suites (e.g., `bazel test //...`) or heavy integration test suites locally. Full verification is handled by remote CI presubmits.
5. **Subagent Communication**: The `code_writer` communicates all results, diffs, and verification outcomes back to the caller agent using `send_message`.
