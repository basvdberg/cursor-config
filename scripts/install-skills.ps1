# Link cursor-config skills into ~/.cursor/skills for Cursor agents.
$ErrorActionPreference = "Stop"
$ConfigRoot = Split-Path -Parent $PSScriptRoot
$SkillsSource = Join-Path $ConfigRoot "skills"
$SkillsTarget = Join-Path $env:USERPROFILE ".cursor\skills"

if (-not (Test-Path $SkillsTarget)) {
    New-Item -ItemType Directory -Path $SkillsTarget -Force | Out-Null
}

Get-ChildItem -Path $SkillsSource -Directory | ForEach-Object {
    $name = $_.Name
    $link = Join-Path $SkillsTarget $name
    if (Test-Path $link) {
        Remove-Item -LiteralPath $link -Force -Recurse
    }
    New-Item -ItemType Junction -Path $link -Target $_.FullName | Out-Null
    Write-Host "Linked $name -> $($_.FullName)"
}

Write-Host "Skills installed under $SkillsTarget"
