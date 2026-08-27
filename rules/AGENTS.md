# Code Writer Kit Guardrails

- **Mandatory Skill Loading Protocol**:
  1. **Always Load Baseline `code-style` Skill**: For **ANY** code modification, the `code_writer` subagent MUST load the baseline `code-style` skill (`skills/code-style/SKILL.md`) from its Available skills list.
  2. **In Addition, Load Language-Specific Skills**: IN ADDITION to `code-style`, the subagent MUST ALSO load the corresponding language-specific skill(s) for the target files being modified (such as `python-style` for Python files via `skills/python-style/SKILL.md`, etc.).
  3. **Workspace Augmentations**: If workspace-specific style skills or workspace root style guidelines (e.g., `<workspace_root>/style_guide.md` or `<workspace_root>/.agents/style_guide.md`) are present, load and augment the guidelines with them, giving project-specific rules precedence in case of conflict.
- **Mandatory Delegation**: All modifications to code and documentation files (`.py`, `.md`) must be performed by the dedicated `code_writer` subagent via `invoke_subagent(TypeName="code_writer", ...)`.
- **Direct Modifications**: Non-code files (e.g. `.json`, `.yaml`, `.txt`, configs) and temporary files (in `scratch/` or `/tmp/`) may be created or edited directly.
- **Targeted Verification**: The `code_writer` subagent may run fast static checks (`ruff`, `pyright`, `mypy`) and isolated, target-specific unit tests, but MUST NEVER execute full-repo monolithic test suites (e.g. `bazel test //...`) or heavy integration test suites locally. Full verification is handled by remote CI presubmits.
