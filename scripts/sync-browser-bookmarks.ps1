# Sync Chrome/Brave merge and BasNAS URLs into browser-bookmarks-sync (Floccus target).
$ErrorActionPreference = "Stop"
$ConfigRoot = Split-Path -Parent $PSScriptRoot
$env:CURSOR_CONFIG_ROOT = $ConfigRoot
$py = Join-Path $PSScriptRoot "sync_browser_bookmarks.py"
$argsList = @($py)
if ($args.Count -gt 0) { $argsList += $args } else { $argsList += @() }
python @argsList
