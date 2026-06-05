#!/usr/bin/env python3
"""Replace private hostnames in markdown prose; preserve config paths and YAML values."""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Files where basnas in examples is intentional (rules about what to avoid)
EXEMPT = {
    "review-markdown-structure/SKILL.md",
}

REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bBasNAS\b"), "local server"),
    (re.compile(r"\bBasnas\b"), "local server"),
    (re.compile(r"\bon basnas\b", re.I), "on the local server"),
    (re.compile(r"\bssh bas@basnas\b"), "ssh $LOCAL_SERVER_SSH"),
    (re.compile(r"\bSSH bas@basnas\b"), "SSH $LOCAL_SERVER_SSH"),
    (re.compile(r"https://([a-z0-9-]+)\.basnas/"), r"https://\1.example/"),
    (re.compile(r"`\*\.basnas`"), "`*.example`"),
    (re.compile(r"\*\.basnas"), "*.example"),
    (re.compile(r"## BasNAS "), "## Local server "),
    (re.compile(r"### BasNAS "), "### Local server "),
    (re.compile(r"# BasNAS "), "# Local server "),
    (re.compile(r"# Deploy container service on BasNAS"), "# Deploy container service on the local server"),
    (re.compile(r"\(BasNAS / QNAP\)"), "(local server / QNAP)"),
    (re.compile(r"BasNAS URL map"), "Local server URL map"),
    (re.compile(r"BasNAS deployment reference"), "Local server deployment reference"),
    (re.compile(r"Fix `admin\.basnas`"), "Fix admin hostname"),
    (re.compile(r"admin\.basnas"), "admin.example"),
    (re.compile(r"Deploy Basnas Container"), "Deploy local server container"),
    (re.compile(r"Basnas Icons"), "Local server icons"),
    (re.compile(r"\+ BasNAS URLs"), "+ local server service URLs"),
    (re.compile(r"BasNAS deploy skill"), "local server deploy skill"),
    (re.compile(r"BasNAS container deploys"), "local server container deploys"),
    (re.compile(r"After BasNAS deploys"), "After local server deploys"),
    (re.compile(r"BasNAS folder"), "local server folder"),
    (re.compile(r"BasNAS service URLs"), "local server service URLs"),
    (re.compile(r"BasNAS deploys"), "local server deploys"),
    (re.compile(r"from BasNAS"), "from the local server"),
    (re.compile(r"on BasNAS"), "on the local server"),
    (re.compile(r"to BasNAS"), "to the local server"),
    (re.compile(r"for BasNAS"), "for the local server"),
    (re.compile(r"## BasNAS layout"), "## Local server layout"),
    (re.compile(r"#basnas-layout"), "#local-server-layout"),
    (re.compile(r"#basnas-deployment"), "#local-server-deployment"),
    (re.compile(r"#step-8-internal-ca-required-for-basnas"), "#step-8-internal-ca-required-for-local-dns-zone"),
    (re.compile(r"required for \.basnas"), "required for the local DNS zone"),
    (re.compile(r"LAN DNS: `\*\.basnas`"), "LAN DNS: `*.example` (zone in local-server.env.example)"),
    (re.compile(r"HTTPS via NGINX \(`\*\.basnas`\)"), "HTTPS via NGINX (local DNS zone)"),
    (re.compile(r"running on basnas on port"), "running on the local server on port"),
    (re.compile(r"SSH session on basnas"), "SSH session on the local server"),
    (re.compile(r"copy from BasNAS"), "copy from the local server"),
    (re.compile(r"\\\\basnas\\"), r"\\\\<local-server>\\"),
    (re.compile(r"<application>\.basnas"), "<application>.<zone>"),
    (re.compile(r"<app>\.basnas"), "<app>.<zone>"),
    (re.compile(r"application\.basnas"), "application.<zone>"),
    (re.compile(r"airflow\.basnas"), "airflow.<zone>"),
    (re.compile(r"nslookup airflow\.basnas"), "nslookup airflow.<zone>"),
    (re.compile(r"\| \*\*basnas\*\*"), "| **local zone**"),
    (re.compile(r"ssl/basnas/"), "ssl/<zone>/"),
    (re.compile(r"/etc/nginx/ssl/basnas/"), "/etc/nginx/ssl/<zone>/"),
    (re.compile(r"nginx/ssl/basnas/"), "nginx/ssl/<zone>/"),
    (re.compile(r"<basnas-lan-ip>"), "${LOCAL_SERVER_LAN_IP}"),
    (re.compile(r"Default `internal` \+ `\.basnas`"), "Default `internal` + local zone"),
    (re.compile(r"required for `\.basnas`"), "required for the local DNS zone"),
    (re.compile(r"private zone`\."), "private zone` (<zone> in local-server.env.example)."),
    (re.compile(r"basnas internal\)"), "local DNS zone in local-server.env.example)"),
    (re.compile(r"not `basnas\.basnas` — conflicts with QNAP short hostname `basnas`"),
     "not `<short-hostname>.<zone>` — avoid duplicating the QNAP short hostname as a subdomain"),
    (re.compile(r"\| `basnas` \(short\)"), "| `<zone>` (short hostname)"),
]

def transform(path: Path, text: str) -> str:
    rel = path.as_posix().replace("\\", "/")
    for exempt in EXEMPT:
        if exempt in rel:
            return text

    new_text = text
    for pattern, repl in REPLACEMENTS:
        if callable(repl):
            new_text = pattern.sub(repl, new_text)
        else:
            new_text = pattern.sub(repl, new_text)
    return new_text


def main(argv: list[str]) -> int:
    roots = [Path(p) for p in argv[1:]] if len(argv) > 1 else [
        Path(__file__).resolve().parent.parent.parent,
    ]
    changed = 0
    for root in roots:
        for path in sorted(root.rglob("*.md")):
            if ".git" in path.parts:
                continue
            original = path.read_text(encoding="utf-8")
            updated = transform(path, original)
            if updated != original:
                path.write_text(updated, encoding="utf-8", newline="\n")
                print(path)
                changed += 1
    print(f"Updated {changed} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
