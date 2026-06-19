#!/bin/sh
# admin.basnas → QTS HTTPS on host :8443 (not host :8080; :58080 is localhost-only)
set -e
export PATH="/share/CACHEDEV1_DATA/.qpkg/container-station/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

CONF_D="/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/conf.d"
QTS_UPSTREAM="${QTS_UPSTREAM:-https://192.168.2.2:8443}"
HTTPS_PORT="${HTTPS_PORT:-443}"
if [ "$HTTPS_PORT" = "443" ]; then
  REDIRECT_TARGET='https://$host$request_uri'
else
  REDIRECT_TARGET="https://\$host:${HTTPS_PORT}\$request_uri"
fi

cat > "${CONF_D}/admin-basnas.conf" <<EOF
# QNAP QTS — https://admin.basnas/ (upstream: host QTS HTTPS :8443)
server {
    listen 80;
    server_name admin.basnas;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 ${REDIRECT_TARGET};
    }
}

server {
    listen 443 ssl;
    http2 on;
    server_name admin.basnas;

    ssl_certificate     /etc/nginx/certs/basnas/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/basnas/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;

    client_max_body_size 0;

    location / {
        proxy_pass ${QTS_UPSTREAM};
        proxy_ssl_server_name on;
        proxy_ssl_verify off;
        proxy_http_version 1.1;
        proxy_set_header Host 192.168.2.2;
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

docker exec nginx-office-c2h nginx -t
docker exec nginx-office-c2h nginx -s reload
echo "admin.basnas upstream -> ${QTS_UPSTREAM}"
