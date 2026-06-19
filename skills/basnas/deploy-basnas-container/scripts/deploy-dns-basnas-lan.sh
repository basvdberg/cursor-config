#!/bin/sh
set -e
mkdir -p /share/CACHEDEV1_DATA/homes/bas/dns-basnas-container
cat > /share/CACHEDEV1_DATA/homes/bas/dns-basnas-container/dnsmasq.conf <<'EOF'
port=53
listen-address=0.0.0.0
bind-interfaces
no-resolv
server=8.8.8.8
server=1.1.1.1
address=/.basnas/192.168.2.2
address=/admin.basnas/192.168.2.2
address=/airflow.basnas/192.168.2.2
address=/immich.basnas/192.168.2.2
address=/plex.basnas/192.168.2.2
address=/radarr.basnas/192.168.2.2
address=/nzbget.basnas/192.168.2.2
address=/qbittorrent.basnas/192.168.2.2
address=/homebridge.basnas/192.168.2.2
log-queries
log-facility=-
EOF

docker rm -f dns-basnas-lan >/dev/null 2>&1 || true
docker run -d --name dns-basnas-lan --restart unless-stopped \
  -p 192.168.2.2:53:53/udp -p 192.168.2.2:53:53/tcp \
  -v /share/CACHEDEV1_DATA/homes/bas/dns-basnas-container/dnsmasq.conf:/etc/dnsmasq.conf:ro \
  strm/dnsmasq

docker ps | grep dns-basnas-lan || true
docker logs --tail 20 dns-basnas-lan || true
