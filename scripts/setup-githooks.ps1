# Point a consumer repository at cursor-config Git hooks.
param(
    [string]$RepoRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path $RepoRoot).Path
$ConfigRoot = Split-Path -Parent $PSScriptRoot

git -C $RepoRoot config core.hooksPath "$ConfigRoot\githooks"
git -C $RepoRoot config cursor.configPath $ConfigRoot
Write-Host "Configured hooks for $(git -C $RepoRoot rev-parse --show-toplevel)"
Write-Host "  core.hooksPath = $ConfigRoot\githooks"
Write-Host "  cursor.configPath = $ConfigRoot"
