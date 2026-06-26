# Apply Cursor user settings required for Wispr Flow IDE integration.
# Wispr side: Settings -> Vibe coding -> Variable recognition (cursorIdeIntegration).
$ErrorActionPreference = "Stop"

$cursorSettingsPath = Join-Path $env:APPDATA "Cursor\User\settings.json"
$required = @{
    "editor.accessibilitySupport" = "on"
}

if (-not (Test-Path $cursorSettingsPath)) {
    Write-Error "Cursor settings not found: $cursorSettingsPath"
}

$raw = Get-Content $cursorSettingsPath -Raw -Encoding UTF8
$settings = $raw | ConvertFrom-Json
$changed = @()

foreach ($key in $required.Keys) {
    $value = $required[$key]
    if (-not ($settings.PSObject.Properties.Name -contains $key) -or $settings.$key -ne $value) {
        $settings | Add-Member -NotePropertyName $key -NotePropertyValue $value -Force
        $changed += "$key = $value"
    }
}

if ($changed.Count -eq 0) {
    Write-Host "Cursor settings already configured for Wispr Flow."
} else {
    $json = $settings | ConvertTo-Json -Depth 100
    Set-Content -Path $cursorSettingsPath -Value $json -Encoding UTF8
    Write-Host "Updated Cursor settings:"
    $changed | ForEach-Object { Write-Host "  $_" }
    Write-Host "Reload Cursor (Developer: Reload Window) for changes to take effect."
}

$wisprConfigPath = Join-Path $env:APPDATA "Wispr Flow\config.json"
if (Test-Path $wisprConfigPath) {
    $wisprRaw = Get-Content $wisprConfigPath -Raw -Encoding UTF8
    $wispr = $wisprRaw | ConvertFrom-Json
    $user = $wispr.prefs.user
    $wisprChanged = $false
    $preferredLanguages = @("en", "nl")
    if (($user.selectedLanguages -join ",") -ne ($preferredLanguages -join ",")) {
        $user.selectedLanguages = $preferredLanguages
        $wispr.prefs.prefsDirty = $true
        $wispr | ConvertTo-Json -Depth 100 | Set-Content -Path $wisprConfigPath -Encoding UTF8
        $wisprChanged = $true
        Write-Host "Updated Wispr Flow selectedLanguages: en, nl (English first)."
    }
    $checks = @(
        @{ Name = "cursorIdeIntegration"; Value = $user.cursorIdeIntegration },
        @{ Name = "ideFileTagging"; Value = $user.ideFileTagging },
        @{ Name = "useAxContext"; Value = $user.useAxContext },
        @{ Name = "selectedLanguages"; Value = ($user.selectedLanguages -join ", ") }
    )
    Write-Host ""
    Write-Host "Wispr Flow config ($wisprConfigPath):"
    foreach ($check in $checks) {
        if ($check.Name -eq "selectedLanguages") {
            Write-Host "  $($check.Name): $($check.Value)"
            continue
        }
        $status = if ($check.Value) { "enabled" } else { "DISABLED - enable in Wispr Flow -> Settings -> Vibe coding" }
        Write-Host "  $($check.Name): $status"
    }
    if (-not $wisprChanged) {
        Write-Host "  selectedLanguages already prefers English."
    }
} else {
    Write-Warning "Wispr Flow config not found. Install Wispr Flow and sign in first."
}

Write-Host ""
Write-Host "Manual checks:"
Write-Host "  1. Wispr Flow running (system tray)"
Write-Host "  2. Settings -> Vibe coding -> Variable recognition ON"
Write-Host "  3. Settings -> Vibe coding -> File tagging in chat ON"
Write-Host "  4. Open target file in an editor tab before dictating"
Write-Host "  5. Click the chat input (sidebar chat, not terminal or inline editor)"
Write-Host ""
Write-Host "File-tagging test phrases (English-first ASR; say kebab names as separate words):"
Write-Host "  - tag data object refresh contract dot md"
Write-Host "  - check at data object refresh contract for errors"
Write-Host "  Say 'dot md' instead of '.md'; speak kebab names as separate words."
Write-Host ""
Write-Host "Success signal in Wispr logs: Paste initiated ... html: yes (file chip paste)."
Write-Host "Plain text only (html: no) means tagging did not match a filename."
