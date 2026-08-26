---
name: code-writer
description: Detailed procedural guide and runbook for delegating code and documentation modifications to the dedicated code_writer subagent.
---

# Code Writer Skill Runbook

This skill defines the complete operational procedure for delegating repository modifications to the dedicated `code_writer` subagent in environments managed by `code-writer-kit`.

## 1. Scope & Guardrails

- **Protected Targets**: All modifications (creations, edits, deletions, and refactors) targeting code or documentation files (specifically `.py` and `.md` extensions) must be executed by the `code_writer` subagent.
- **Unprotected / Exempt Targets**: Direct writes by the root agent are permitted for non-code files (e.g., `.json`, `.yaml`, `.toml`, `.txt`, configuration manifests) and temporary workspace paths (e.g., paths matching `/scratch/`, `/tmp/`, or `.system_generated`).
- **Hook Enforcement**: The PreToolUse hook (`scripts/enforce_writer.py`) intercepts unauthorized file operations on protected targets and returns a hard block instructing delegation.

## 2. Step-by-Step Delegation Procedure

### Step 1: Inspect Style & Architectural Guidelines
Read the repository style guide at `style_guide.md` to load the exact architectural requirements, coding conventions, type annotation rules, and docstring formats.

### Step 2: Define the `code_writer` Subagent
Register or configure the `code_writer` subagent by invoking `define_subagent` with `enable_write_tools=true` and passing the exact contents of `style_guide.md` as the `system_prompt`:

```json
{
  "name": "code_writer",
  "enable_write_tools": true,
  "system_prompt": "<contents of style_guide.md>"
}
```

### Step 3: Invoke the `code_writer` Subagent
Dispatch the subagent using `invoke_subagent` with a detailed prompt including target files, operational requirements, behavioral constraints, and verification instructions:

```json
{
  "TypeName": "code_writer",
  "Role": "Code Writer",
  "Prompt": "Implement feature X in src/feature.py according to style guidelines. Ensure caller-before-callee order, strict type annotations, and Google-style docstrings."
}
```

### Step 4: Validate Subagent Deliverables
Review the completion report and file modifications returned by the subagent via `send_message`. Verify that changes strictly adhere to all architectural rules.

## 3. Operational Invariants

1. **Mandatory Subagent Delegation**: Never bypass `code_writer` when authoring or editing protected `.py` or `.md` files.
2. **Style Guide Fidelity**: The `system_prompt` supplied during `define_subagent` must accurately reflect the contents of `style_guide.md`.
3. **Verification Policy**:
   - The `code_writer` subagent may execute fast static checks (`ruff check`, `ruff format --check`, `pyright`, `mypy`) and isolated, target-specific unit tests to validate syntax and behavior.
   - The subagent MUST NEVER execute full-repo monolithic test suites (e.g., `bazel test //...`) or heavy integration test suites locally. Full verification is handled by remote CI presubmits.
4. **Subagent Communication**: The `code_writer` communicates all results, diffs, and verification outcomes back to the caller agent using `send_message`.
