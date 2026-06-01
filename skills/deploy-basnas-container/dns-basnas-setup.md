# Fix `admin.basnas` not resolving

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

**NGINX** for `admin.basnas` is already installed on BasNAS (`/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/conf.d/admin-basnas.conf`).

## Fix A — Windows (fastest, this PC)

1. Right-click **`scripts/add-basnas-hosts-admin.cmd`** → **Run as administrator**
2. Or manually add to `C:\Windows\System32\drivers\etc\hosts`:

```text
192.168.2.2 admin.basnas airflow.basnas immich.basnas kafka.basnas jobhunter.basnas
```

3. `ipconfig /flushdns`
4. Open: **https://admin.basnas:9443/** (install CA below) or test **http://admin.basnas:9080/**

## Fix B — QNAP DNS (all LAN devices)

In your **SSH session on basnas** (password required):

```bash
sudo sh /tmp/setup-qnap-dns-basnas.sh
```

Then on the router, set **DHCP DNS server** to **192.168.2.2** (BasNAS), or add static local DNS records for `*.basnas` → `192.168.2.2`.

## Trust HTTPS (internal CA)

Install once on Windows:

```text
\\basnas\... or copy from BasNAS:
/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/certs/basnas-ca.crt

Install on Windows (one-time, per PC): `scripts/install-windows-basnas-ca.ps1`
```

Double-click → Install → **Local Machine** → **Trusted Root Certification Authorities**.

## URLs until port 443 is remapped

| Service | URL |
|---------|-----|
| QTS admin | https://admin.basnas:9443/ |
| (interim HTTP) | http://admin.basnas:9080/ → redirects to HTTPS |

After NGINX uses host **443**, use `https://admin.basnas/` without port.

## Verify

```powershell
nslookup admin.basnas
curl.exe -kI --resolve admin.basnas:9443:192.168.2.2 https://admin.basnas:9443/
```

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../../readme.md)
  - Githooks
  - Skills
    - Browser Bookmarks Sync
      - [Browser bookmarks sync](../browser-bookmarks-sync/SKILL.md)
    - Create Design Pattern
      - [Create design pattern](../create-design-pattern/SKILL.md)
      - [{Title}](../create-design-pattern/TEMPLATE.md)
    - Deploy Basnas Container
      - Templates
      - [Fix `admin.basnas` not resolving](dns-basnas-setup.md)
      - [Examples](examples.md)
      - [NGINX as HTTPS edge on port 443 (BasNAS / QNAP)](nginx-on-443.md)
      - [BasNAS deployment reference](reference.md)
      - [Deploy container service on BasNAS](SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.basnas)](troubleshooting-tls.md)
      - [BasNAS URL map](url-map.md)
    - Markdown Project Structure
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](../markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](../review-markdown-structure/SKILL.md)
- Related repositories
  - [Browser bookmarks sync](https://github.com/basvdberg/browser-bookmarks-sync)
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026)
<!-- markdown-project-structure:end -->
