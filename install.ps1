<#
.SYNOPSIS
    Installs the Antigravity code-writer-kit plugin on Windows.

.DESCRIPTION
    Installs code-writer-kit globally or in a workspace, registering hooks, rules, and skills.

.PARAMETER Global
    Install globally to ~/.gemini/config/plugins/code-writer-kit (default).

.PARAMETER Workspace
    Install to workspace .agents/plugins/code-writer-kit.

.PARAMETER WorkspaceDir
    Custom workspace root directory path.

.PARAMETER Symlink
    Create a symbolic link instead of copying files.

.PARAMETER Uninstall
    Remove code-writer-kit and clean up configuration.

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Workspace
    .\install.ps1 -Symlink
    .\install.ps1 -Uninstall
#>
[CmdletBinding(DefaultParameterSetName = 'Install')]
param (
    [Parameter(ParameterSetName = 'Install')]
    [switch]$Global = $true,

    [Parameter(ParameterSetName = 'Install')]
    [switch]$Workspace,

    [Parameter()]
    [string]$WorkspaceDir = "",

    [Parameter(ParameterSetName = 'Install')]
    [switch]$Symlink,

    [Parameter(ParameterSetName = 'Uninstall')]
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$PyArgs = @()

if ($Uninstall) {
    $PyArgs += "--uninstall"
}

if ($Workspace) {
    $PyArgs += "--workspace"
} else {
    $PyArgs += "--global"
}

if ($WorkspaceDir) {
    $PyArgs += "--workspace-dir"
    $PyArgs += $WorkspaceDir
}

if ($Symlink) {
    $PyArgs += "--symlink"
}

$PythonCmd = "python"
if (-not (Get-Command $PythonCmd -ErrorAction SilentlyContinue)) {
    if (Get-Command "py" -ErrorAction SilentlyContinue) {
        $PythonCmd = "py"
    } else {
        Write-Error "Python 3 is required to run the installer, but was not found in PATH."
        exit 1
    }
}

& $PythonCmd "$ScriptDir\install.py" @PyArgs
exit $LASTEXITCODE
