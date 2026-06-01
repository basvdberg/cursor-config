#!/bin/sh
# Deploy https://<app>.basnas/ vhosts on nginx-office-c2h (run on BasNAS via SSH).
set -e

DOCKER="${DOCKER:-/share/CACHEDEV1_DATA/.qpkg/container-station/bin/docker}"
NGINX_DIR="${NGINX_DIR:-/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h}"
CONF_D="${NGINX_DIR}/conf.d"
CERT_DIR="${NGINX_DIR}/certs/basnas"
BASNAS_IP="${BASNAS_IP:-192.168.2.2}"

mkdir -p "$CONF_D" "$CERT_DIR"

# Ensure internal CA exists (admin-basnas may have created it)
if [ ! -f "$CERT_DIR/fullchain.pem" ]; then
  echo "Missing $CERT_DIR/fullchain.pem — run setup-admin-basnas-nginx.sh first." >&2
  exit 1
fi

write_vhost() {
  app="$1"
  server_name="$2"
  upstream="$3"
  extra="${4:-}"

  conf="${CONF_D}/${app}-basnas.conf"
  cat > "$conf" <<EOF
# https://${server_name}/ — internal zone
server {
    listen 80;
    listen [::]:80;
    server_name ${server_name};

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name ${server_name};

    ssl_certificate     /etc/nginx/certs/basnas/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/basnas/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;

    ${extra}

    location / {
        proxy_pass http://${upstream};
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
EOF
  echo "  wrote ${conf}"
}

IMMICH_EXTRA='client_max_body_size 800M;'

echo "=== Connecting nginx to app Docker networks ==="
for net in apache-airflow_default kafka_default immich_default jobhunter_default bridge; do
  $DOCKER network connect "$net" nginx-office-c2h 2>/dev/null || true
done

echo "=== Writing *.basnas vhosts ==="
write_vhost airflow airflow.basnas "airflow-standalone:8080"
write_vhost kafka kafka.basnas "kafka-ui:8080"
write_vhost immich immich.basnas "immich_server:2283" "$IMMICH_EXTRA"
write_vhost jobhunter jobhunter.basnas "jobhunter-app:8080"

# Default bridge (lxcbr0) — container IP; nginx is on bridge network
RADARR_IP="$($DOCKER inspect radarr-3 --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')"
NZBGET_IP="$($DOCKER inspect nzbget-2 --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')"
write_vhost radarr radarr.basnas "${RADARR_IP}:7878"
write_vhost nzbget nzbget.basnas "${NZBGET_IP}:6789"

HOMEBRIDGE_IP="$($DOCKER inspect homebridge-2 --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 2>/dev/null | head -1)"
HOMEBRIDGE_IP="${HOMEBRIDGE_IP:-192.168.2.36}"
write_vhost homebridge homebridge.basnas "${HOMEBRIDGE_IP}:8581"

if $DOCKER ps --format '{{.Names}}' | grep -qx qbittorrent-1; then
  QBIT_PORT="$($DOCKER port qbittorrent-1 8080/tcp 2>/dev/null | head -1 | sed 's/.*://')"
  QBIT_PORT="${QBIT_PORT:-32772}"
  write_vhost qbittorrent qbittorrent.basnas "${BASNAS_IP}:${QBIT_PORT}"
else
  echo "  skip qbittorrent.basnas (container qbittorrent-1 not running)"
fi

echo "=== Reload nginx ==="
$DOCKER exec nginx-office-c2h nginx -t
$DOCKER exec nginx-office-c2h nginx -s reload

echo "=== Done. Test from LAN: curl -kI https://airflow.basnas/ ==="
