# Install all shared Cursor assets (user skills). Rules live only in cursor-config/rules/.
$ErrorActionPreference = "Stop"
$Scripts = Split-Path -Parent $MyInvocation.MyCommand.Path

& (Join-Path $Scripts "install-skills.ps1")

Write-Host "Cursor config installed (skills)."
