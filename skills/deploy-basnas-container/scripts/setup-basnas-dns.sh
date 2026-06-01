#!/bin/sh
# LAN DNS for *.basnas on BasNAS (dnsmasq). Run on QNAP as user with docker access.
set -e

BASNAS_IP="${BASNAS_IP:-192.168.2.2}"
DNS_DIR="/share/CACHEDEV1_DATA/homes/bas/dns-basnas"
CONTAINER_NAME="dns-basnas"

mkdir -p "$DNS_DIR"

cat > "$DNS_DIR/dnsmasq.conf" <<EOF
# LAN DNS for internal *.basnas zone
listen-address=0.0.0.0
port=53

# Do not use /etc/resolv.conf inside container for upstream
no-resolv
server=192.168.2.254
server=1.1.1.1

# Internal zone → BasNAS (NGINX)
address=/basnas/${BASNAS_IP}
address=/.basnas/${BASNAS_IP}

# Explicit hosts
address=/admin.basnas/${BASNAS_IP}
address=/airflow.basnas/${BASNAS_IP}
address=/immich.basnas/${BASNAS_IP}
address=/kafka.basnas/${BASNAS_IP}
address=/jobhunter.basnas/${BASNAS_IP}
address=/plex.basnas/${BASNAS_IP}
address=/radarr.basnas/${BASNAS_IP}
address=/nzbget.basnas/${BASNAS_IP}
address=/qbittorrent.basnas/${BASNAS_IP}
address=/homebridge.basnas/${BASNAS_IP}
address=/adguard.basnas/${BASNAS_IP}

log-queries
log-facility=-
EOF

echo "Stopping old $CONTAINER_NAME if present..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting dnsmasq..."
# Prefer host network so LAN clients can use ${BASNAS_IP}:53 (QNAP may already bind 53 on host)
if docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  --network host \
  -v "$DNS_DIR/dnsmasq.conf:/etc/dnsmasq.conf:ro" \
  strm/dnsmasq 2>/tmp/dns-basnas.err; then
  echo "dnsmasq started with --network host"
else
  echo "Host network failed, trying published ports 53..."
  docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
  docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p 53:53/tcp -p 53:53/udp \
    -v "$DNS_DIR/dnsmasq.conf:/etc/dnsmasq.conf:ro" \
    strm/dnsmasq
fi

echo "Testing from container host..."
sleep 2
if command -v nslookup >/dev/null 2>&1; then
  nslookup admin.basnas "${BASNAS_IP}" || nslookup admin.basnas 127.0.0.1
fi

echo ""
echo "Done. Set router DHCP DNS server to: ${BASNAS_IP}"
echo "Or on Windows (Admin PowerShell):"
echo "  Add-DnsClientNrptRule -Namespace '.basnas' -NameServers '${BASNAS_IP}'"
