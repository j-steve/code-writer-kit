"""Installer CLI for the Antigravity code-writer-kit plugin.

Supports global and workspace installations, file copying, symbolic linking,
and automated registration into Antigravity configuration files.
"""

import argparse
import json
import os
import shutil
import sys
from typing import Optional


class AppException(Exception):
    """Base application exception for code writer installer."""


class InstallationError(AppException):
    """Raised when filesystem operations during installation fail."""


class ConfigurationError(AppException):
    """Raised when reading or updating the configuration JSON fails."""


def parse_arguments(args: list[str]) -> argparse.Namespace:
    """Parses command-line arguments for plugin installation.

    Args:
        args: List of argument strings passed from CLI.

    Returns:
        Parsed arguments namespace object.
    """
    parser = argparse.ArgumentParser(
        description="Installer CLI for Antigravity code-writer-kit plugin."
    )
    parser.add_argument(
        "--global",
        dest="is_global",
        action="store_true",
        default=True,
        help="Install globally to ~/.gemini/config/plugins/ (default)."
    )
    parser.add_argument(
        "--workspace",
        dest="is_workspace",
        action="store_true",
        default=False,
        help="Install locally into the active workspace (.agents/plugins/)."
    )
    parser.add_argument(
        "--workspace-dir",
        type=str,
        default="",
        help="Custom root directory for workspace installation."
    )
    parser.add_argument(
        "--symlink",
        "--link",
        dest="use_symlink",
        action="store_true",
        default=False,
        help="Create a filesystem symlink instead of copying files."
    )
    parser.add_argument(
        "--uninstall",
        dest="uninstall",
        action="store_true",
        default=False,
        help="Uninstall the plugin and remove configuration entries."
    )
    return parser.parse_args(args)


def resolve_target_dir(is_global: bool, workspace_dir: str) -> str:
    """Calculates the target installation directory path.

    Args:
        is_global: Whether to install to the global user plugins directory.
        workspace_dir: Custom workspace path if workspace mode is active.

    Returns:
        Absolute destination directory path string.
    """
    plugin_name: str = "code-writer-kit"
    if is_global:
        home_dir: str = os.path.expanduser("~")
        return os.path.join(home_dir, ".gemini", "config", "plugins", plugin_name)
    base_root: str = workspace_dir if workspace_dir else os.getcwd()
    return os.path.join(base_root, ".agents", "plugins", plugin_name)


def resolve_config_path(is_global: bool, workspace_dir: str) -> str:
    """Calculates the configuration file path to update.

    Args:
        is_global: Whether installing to global user configuration.
        workspace_dir: Custom workspace path if workspace mode is active.

    Returns:
        Absolute configuration file path string.
    """
    if is_global:
        home_dir: str = os.path.expanduser("~")
        return os.path.join(home_dir, ".gemini", "config", "config.json")
    base_root: str = workspace_dir if workspace_dir else os.getcwd()
    return os.path.join(base_root, ".agents", "config.json")


def copy_plugin_files(source_dir: str, target_dir: str) -> None:
    """Copies the plugin file tree to the target directory.

    Args:
        source_dir: Source code-writer-kit directory.
        target_dir: Target destination plugin directory.

    Raises:
        InstallationError: If file copying fails due to I/O error.
    """
    try:
        if os.path.exists(target_dir):
            if os.path.islink(target_dir):
                os.unlink(target_dir)
            else:
                shutil.rmtree(target_dir)
        shutil.copytree(
            source_dir,
            target_dir,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git")
        )
    except OSError as exc:
        raise InstallationError(f"Failed to copy files to {target_dir}") from exc


def create_plugin_symlink(source_dir: str, target_dir: str) -> None:
    """Creates a symbolic link pointing to the source plugin directory.

    Args:
        source_dir: Source code-writer-kit directory.
        target_dir: Destination symlink path.

    Raises:
        InstallationError: If symlink creation fails.
    """
    try:
        parent_dir: str = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)
        if os.path.exists(target_dir) or os.path.islink(target_dir):
            if os.path.islink(target_dir) or os.path.isfile(target_dir):
                os.unlink(target_dir)
            else:
                shutil.rmtree(target_dir)
        os.symlink(source_dir, target_dir, target_is_directory=True)
    except OSError as exc:
        raise InstallationError(
            f"Failed to symlink {source_dir} -> {target_dir}"
        ) from exc


def update_antigravity_config(
    config_path: str, plugin_name: str, enabled: bool
) -> None:
    """Updates the config.json file to enable or disable the plugin.

    Args:
        config_path: Path to the target config.json file.
        plugin_name: Name of the plugin key in the config.
        enabled: State to record for the plugin.

    Raises:
        ConfigurationError: If config file cannot be read or written.
    """
    try:
        parent_dir: str = os.path.dirname(config_path)
        os.makedirs(parent_dir, exist_ok=True)
        data: dict[str, object] = {}
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as file_handle:
                content: str = file_handle.read().strip()
                if content:
                    raw: object = json.loads(content)
                    if isinstance(raw, dict):
                        data = {str(k): v for k, v in raw.items()}
        plugins_obj: object = data.get("plugins")
        plugins_dict: dict[str, object] = (
            {str(k): v for k, v in plugins_obj.items()}
            if isinstance(plugins_obj, dict)
            else {}
        )
        if enabled:
            plugins_dict[plugin_name] = {"enabled": True}
        else:
            plugins_dict.pop(plugin_name, None)
        data["plugins"] = plugins_dict
        with open(config_path, "w", encoding="utf-8") as file_handle:
            json.dump(data, file_handle, indent=2)
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigurationError(
            f"Failed to update config at {config_path}"
        ) from exc


def perform_install(
    source_dir: str,
    target_dir: str,
    config_path: str,
    use_symlink: bool
) -> None:
    """Executes the full installation workflow.

    Args:
        source_dir: Root directory of code-writer-kit.
        target_dir: Destination plugin path.
        config_path: Target configuration JSON path.
        use_symlink: Whether to link instead of copying.

    Raises:
        InstallationError: If installation fails.
        ConfigurationError: If configuration update fails.
    """
    print(f"Installing code-writer-kit to: {target_dir}")
    if use_symlink:
        create_plugin_symlink(source_dir, target_dir)
    else:
        copy_plugin_files(source_dir, target_dir)
    update_antigravity_config(config_path, "code-writer-kit", enabled=True)
    print(f"Successfully configured in: {config_path}")


def perform_uninstall(target_dir: str, config_path: str) -> None:
    """Removes installed plugin files and updates configuration.

    Args:
        target_dir: Destination plugin path to remove.
        config_path: Configuration JSON path to update.

    Raises:
        InstallationError: If removal of plugin files fails.
        ConfigurationError: If configuration update fails.
    """
    print(f"Removing code-writer-kit from: {target_dir}")
    try:
        if os.path.islink(target_dir) or os.path.isfile(target_dir):
            os.unlink(target_dir)
        elif os.path.isdir(target_dir):
            shutil.rmtree(target_dir)
    except OSError as exc:
        raise InstallationError(
            f"Failed to remove directory {target_dir}"
        ) from exc
    if os.path.exists(config_path):
        update_antigravity_config(config_path, "code-writer-kit", enabled=False)
        print(f"Updated configuration in: {config_path}")


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entrypoint for installer execution.

    Args:
        argv: Optional list of argument strings. Defaults to sys.argv[1:].

    Returns:
        Integer exit code (0 for success, non-zero for failure).
    """
    args_list: list[str] = argv if argv is not None else sys.argv[1:]
    args: argparse.Namespace = parse_arguments(args_list)
    is_global: bool = not args.is_workspace
    source_dir: str = os.path.dirname(os.path.abspath(__file__))
    target_dir: str = resolve_target_dir(is_global, args.workspace_dir)
    config_path: str = resolve_config_path(is_global, args.workspace_dir)

    try:
        if args.uninstall:
            perform_uninstall(target_dir, config_path)
            print("code-writer-kit has been uninstalled successfully.")
        else:
            perform_install(source_dir, target_dir, config_path, args.use_symlink)
            print("code-writer-kit installed and activated successfully!")
        return 0
    except AppException as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
