# Fix admin hostname not resolving

## Table of contents

<!-- markdown-toc:start -->
- [Cause](#cause)
- [Fix A — Windows (fastest, this PC)](#fix-a-windows-fastest-this-pc)
- [Fix B — QNAP DNS (all LAN devices)](#fix-b-qnap-dns-all-lan-devices)
- [Trust HTTPS (internal CA)](#trust-https-internal-ca)
- [URLs until port 443 is remapped](#urls-until-port-443-is-remapped)
- [Verify](#verify)
<!-- markdown-toc:end -->

## Cause

`.basnas` is a **private zone**. Your router (`192.168.2.254`) does not know it. QNAP dnsmasq was not listening on the LAN IP (`192.168.2.2`) for custom records until configured.

**NGINX** for `admin.example` is already installed on local server (`/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/conf.d/admin-basnas.conf`).

## Fix A — Windows (fastest, this PC)

1. Right-click **`scripts/add-basnas-hosts-admin.cmd`** → **Run as administrator**
2. Or manually add to `C:\Windows\System32\drivers\etc\hosts`:

```text
See [hosts.example](hosts.example) (copy the line into your hosts file; values match [local-server.env.example](local-server.env.example))
```

3. `ipconfig /flushdns`
4. Open: **https://admin.example:9443/** (install CA below) or test **http://admin.example:9080/**

## Fix B — QNAP DNS (all LAN devices)

In your **SSH session on the local server** (password required):

```bash
sudo sh /tmp/setup-qnap-dns-basnas.sh
```

Then on the router, set **DHCP DNS server** to **192.168.2.2** (local server), or add static local DNS records for `*.example` → `192.168.2.2`.

## Trust HTTPS (internal CA)

Install once on Windows:

```text
\\<local-server>\... or copy from local server:
/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/certs/basnas-ca.crt

Install on Windows (one-time, per PC): `scripts/install-windows-basnas-ca.ps1`
```

Double-click → Install → **Local Machine** → **Trusted Root Certification Authorities**.

## URLs until port 443 is remapped

| Service | URL |
|---------|-----|
| QTS admin | https://admin.example:9443/ |
| (interim HTTP) | http://admin.example:9080/ → redirects to HTTPS |

After NGINX uses host **443**, use `https://admin.example/` without port.

## Verify

```powershell
nslookup admin.example
curl.exe -kI --resolve admin.example:9443:192.168.2.2 https://admin.example:9443/
```
