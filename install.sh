#!/usr/bin/env bash
#
# Installer for Antigravity code-writer-kit on macOS/Linux.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "Error: Python is required to run the installer, but was not found." >&2
    exit 1
fi

exec "$PYTHON_CMD" "$SCRIPT_DIR/install.py" "$@"
