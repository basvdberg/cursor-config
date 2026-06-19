# Run once as Administrator on Windows — resolves *.basnas via BasNAS dnsmasq
# Requires dns-basnas container running on 192.168.2.2

$BasnasIp = "192.168.2.2"

# NRPT: send all .basnas queries to BasNAS DNS
$existing = Get-DnsClientNrptRule -ErrorAction SilentlyContinue | Where-Object { $_.Namespace -eq ".basnas" }
if ($existing) {
    Set-DnsClientNrptRule -Namespace ".basnas" -NameServers $BasnasIp -DisplayName "BasNAS internal" -ErrorAction SilentlyContinue
} else {
    Add-DnsClientNrptRule -Namespace ".basnas" -NameServers $BasnasIp -DisplayName "BasNAS internal"
}

# Fallback hosts file (all app hostnames)
$hostsLine = "$BasnasIp`tadmin.basnas airflow.basnas immich.basnas radarr.basnas nzbget.basnas qbittorrent.basnas homebridge.basnas plex.basnas adguard.basnas"
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hosts = Get-Content $hostsPath -Raw
if ($hosts -notmatch "admin\.basnas") {
    Add-Content -Path $hostsPath -Value "`n# BasNAS internal zone`n$hostsLine"
    Write-Host "Added admin.basnas to hosts file."
}

Clear-DnsClientCache
Write-Host "DNS configured. Test: ping admin.basnas"
Resolve-DnsName admin.basnas -ErrorAction SilentlyContinue
