#!/bin/sh
# admin.basnas → QTS via nginx-office-c2h (matches existing office.c2h.nl vhost style)
set -e

NGINX_DIR="/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h"
CONF_D="${NGINX_DIR}/conf.d"
CERT_DIR="${NGINX_DIR}/certs/basnas"
# QTS admin HTTPS (not :8080 — that is jobhunter on this host)
QTS_UPSTREAM="${QTS_UPSTREAM:-https://192.168.2.2:8443}"
HTTPS_PORT="${HTTPS_PORT:-443}"
if [ "$HTTPS_PORT" = "443" ]; then
  REDIRECT_TARGET='https://\$host\$request_uri'
else
  REDIRECT_TARGET="https://\$host:${HTTPS_PORT}\$request_uri"
fi

mkdir -p "$CERT_DIR" "$CONF_D"

# Internal CA + wildcard *.basnas (skip if fullchain already exists)
if [ ! -f "$CERT_DIR/fullchain.pem" ]; then
  echo "Creating internal CA and *.basnas certificate..."
  CA_KEY="${NGINX_DIR}/certs/basnas-ca.key"
  CA_CRT="${NGINX_DIR}/certs/basnas-ca.crt"
  if [ ! -f "$CA_CRT" ]; then
    openssl genrsa -out "$CA_KEY" 4096
    openssl req -x509 -new -nodes -key "$CA_KEY" -sha256 -days 3650 \
      -subj "/CN=BasNAS Home CA" -out "$CA_CRT"
  fi
  openssl genrsa -out "$CERT_DIR/privkey.pem" 2048
  cat > /tmp/basnas-openssl.cnf <<EOF
[req]
distinguished_name = dn
req_extensions = ext
prompt = no
[dn]
CN = BasNAS Internal
[ext]
subjectAltName = @alt
[alt]
DNS.1 = basnas
DNS.2 = *.basnas
DNS.3 = admin.basnas
EOF
  openssl req -new -key "$CERT_DIR/privkey.pem" -out /tmp/basnas.csr -config /tmp/basnas-openssl.cnf
  openssl x509 -req -in /tmp/basnas.csr -CA "$CA_CRT" -CAkey "$CA_KEY" -CAcreateserial \
    -out "$CERT_DIR/cert.pem" -days 825 -sha256 -extfile /tmp/basnas-openssl.cnf -extensions ext
  cat "$CERT_DIR/cert.pem" "$CA_CRT" > "$CERT_DIR/fullchain.pem"
  echo "CA root (install on PCs): $CA_CRT"
fi

cat > "${CONF_D}/admin-basnas.conf" <<EOF
# QNAP QTS — https://admin.basnas/
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

echo "Reloading nginx-office-c2h..."
docker exec nginx-office-c2h nginx -t
docker exec nginx-office-c2h nginx -s reload

echo "admin.basnas vhost installed. HTTPS on host ports 9080 (http) / 9443 (https) until 443 is remapped."
echo "Test from LAN PC:"
echo "  curl -kI --resolve admin.basnas:9443:192.168.2.2 https://admin.basnas:9443/"
echo "  (requires admin.basnas in DNS or hosts file)"
