# Link cursor-config skills into ~/.cursor/skills for Cursor agents.
# Discovers SKILL.md recursively; junctions each leaf skill folder flat by skill name.
$ErrorActionPreference = "Stop"
$ConfigRoot = Split-Path -Parent $PSScriptRoot
$SkillsSource = Join-Path $ConfigRoot "skills"
$SkillsTarget = Join-Path $env:USERPROFILE ".cursor\skills"

if (-not (Test-Path $SkillsTarget)) {
    New-Item -ItemType Directory -Path $SkillsTarget -Force | Out-Null
}

$skillDirs = @(
    Get-ChildItem -Path $SkillsSource -Recurse -Filter "SKILL.md" -File |
        ForEach-Object { $_.Directory.FullName }
)

$installedNames = @{}
foreach ($skillDir in $skillDirs) {
    $name = Split-Path -Leaf $skillDir
    if ($installedNames.ContainsKey($name)) {
        Write-Error "Duplicate skill name '$name': $($installedNames[$name]) and $skillDir"
    }
    $installedNames[$name] = $skillDir

    $link = Join-Path $SkillsTarget $name
    if (Test-Path $link) {
        Remove-Item -LiteralPath $link -Force -Recurse
    }
    New-Item -ItemType Junction -Path $link -Target $skillDir | Out-Null
    Write-Host "Linked $name -> $skillDir"
}

Get-ChildItem -Path $SkillsTarget -Directory | ForEach-Object {
    if (-not $installedNames.ContainsKey($_.Name)) {
        Remove-Item -LiteralPath $_.FullName -Force -Recurse
        Write-Host "Removed stale junction $($_.Name)"
    }
}

Write-Host "Skills installed under $SkillsTarget ($($installedNames.Count) skills)"
