# Install BasNAS internal CA so https://*.basnas/ is trusted in browsers (uses Windows cert store).
# Requires: SSH host "basnas", or pass -CaCertPath to a local basnas-ca.crt copy.
param(
    [string]$CaCertPath,
    [switch]$MachineStore
)

$ErrorActionPreference = "Stop"
$remoteCa = "/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/certs/basnas-ca.crt"

if (-not $CaCertPath) {
    $CaCertPath = Join-Path $env:TEMP "basnas-ca.crt"
    $sshHost = if ($env:BASNAS_SSH) { $env:BASNAS_SSH } else { "bas@192.168.2.2" }
    scp "${sshHost}:${remoteCa}" $CaCertPath
}

if (-not (Test-Path $CaCertPath)) {
    throw "CA file not found: $CaCertPath"
}

if ($MachineStore) {
    certutil -addstore Root $CaCertPath | Out-Null
} else {
    certutil -addstore -user Root $CaCertPath | Out-Null
}

Write-Host "Installed. Test: curl.exe -I https://admin.basnas/"
Write-Host "CA file kept at: $CaCertPath"
