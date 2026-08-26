"""Enforces code_writer subagent delegation for repository write operations.

This module acts as an Antigravity PreToolUse hook for file modification tools,
ensuring that direct writes by root agents to protected code and documentation
files are intercepted and redirected to the dedicated code_writer subagent.
"""

from __future__ import annotations

import json
import os
import re
import sys

_PROTECTED_EXTENSIONS: tuple[str, ...] = (".py", ".md")
_EXCLUDED_PATH_SUBSTRINGS: tuple[str, ...] = (
    "/scratch/",
    "/tmp/",
    ".system_generated",
)


class AppException(Exception):
    """Base application exception for code writer enforcement."""


class HookPayloadError(AppException):
    """Raised when the hook input payload is malformed or invalid."""


def main() -> None:
    """Main entrypoint for the PreToolUse hook execution."""
    result: dict[str, str] = execute_guard()
    print(json.dumps(result))


def execute_guard() -> dict[str, str]:
    """Evaluates the hook context and determines permission.

    Returns:
        Decision dictionary conforming to the Antigravity PreToolUse hook spec.
    """
    try:
        payload: dict[str, object] = read_hook_payload()
    except HookPayloadError:
        return {"decision": "allow"}

    target_file: str = extract_target_file(payload)
    if not is_protected_target(target_file):
        return {"decision": "allow"}

    transcript_path: str = str(payload.get("transcriptPath", ""))
    if is_authorized_writer(transcript_path):
        return {"decision": "allow"}

    guide_path: str = resolve_style_guide_path()
    return build_deny_response(target_file, guide_path)


def read_hook_payload() -> dict[str, object]:
    """Reads and parses the JSON hook payload from standard input.

    Returns:
        A dictionary containing the parsed hook payload.

    Raises:
        HookPayloadError: If standard input cannot be parsed as JSON.
    """
    try:
        raw_data: str = sys.stdin.read().strip()
        if not raw_data:
            return {}
        parsed_data: object = json.loads(raw_data)
        if isinstance(parsed_data, dict):
            return {str(key): val for key, val in parsed_data.items()}
        return {}
    except Exception as exc:
        raise HookPayloadError("Failed to parse stdin JSON payload.") from exc


def extract_target_file(payload: dict[str, object]) -> str:
    """Extracts the target file path from tool call arguments in the payload.

    Args:
        payload: Hook input payload dictionary.

    Returns:
        Target file path or an empty string if not present.
    """
    tool_call: object = payload.get("toolCall")
    if not isinstance(tool_call, dict):
        return ""
    args: object = tool_call.get("args")
    if not isinstance(args, dict):
        return ""
    target: object = args.get("TargetFile") or args.get("target_file") or ""
    return str(target) if target else ""


def is_protected_target(target_file: str) -> bool:
    """Determines whether a target file is subject to code_writer enforcement.

    Args:
        target_file: File system path of the target file.

    Returns:
        True if target file matches protected extensions and is not excluded.
    """
    if not target_file:
        return False
    normalized: str = target_file.replace("\\", "/")
    if any(excluded in normalized for excluded in _EXCLUDED_PATH_SUBSTRINGS):
        return False
    return normalized.endswith(_PROTECTED_EXTENSIONS)


def is_authorized_writer(transcript_path: str) -> bool:
    """Inspects the session transcript to verify code_writer authorization.

    Args:
        transcript_path: File system path to the active transcript JSONL.

    Returns:
        True if the current caller is verified as the code_writer subagent.
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return False
    try:
        with open(transcript_path, "r", encoding="utf-8") as file_handle:
            transcript_content: str = file_handle.read()
        pattern: str = (
            r'("TypeName"|"typeName"|"name"|"role")\s*:\s*'
            r'"(code_writer|Code\s*Writer)"'
        )
        return bool(re.search(pattern, transcript_content, re.IGNORECASE))
    except (OSError, UnicodeDecodeError):
        return False


def resolve_style_guide_path() -> str:
    """Resolves the absolute path to the bundled style guide file.

    Returns:
        Normalized absolute path string to style_guide.md.
    """
    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "style_guide.md"))


def build_deny_response(target_file: str, guide_path: str) -> dict[str, str]:
    """Constructs a hard-block decision dictionary for unauthorized writes.

    Args:
        target_file: The file path targeted by the write operation.
        guide_path: Absolute path to the style guide file.

    Returns:
        Dictionary payload containing the denial decision and instructions.
    """
    reason_lines: list[str] = [
        f"HARD BLOCK: Direct modification of '{target_file}' by the root agent is disallowed.",
        "",
        "MANDATORY ACTION REQUIRED:",
        f"1. Read the style guide from: {guide_path}",
        "2. Call `define_subagent` with name='code_writer', enable_write_tools=True, and set `system_prompt` to the EXACT contents of that file.",
        "3. Call `invoke_subagent(TypeName='code_writer', ...)` with the coding task to execute the change.",
    ]
    return {
        "decision": "deny",
        "reason": "\n".join(reason_lines),
    }


if __name__ == "__main__":
    main()
