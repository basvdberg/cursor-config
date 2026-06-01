#!/bin/sh
# Re-issue *.basnas leaf cert with explicit SANs (Windows Schannel rejects wildcard-only *.basnas).
set -e

NGINX_DIR="${NGINX_DIR:-/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h}"
CERT_DIR="${NGINX_DIR}/certs/basnas"
CA_KEY="${NGINX_DIR}/certs/basnas-ca.key"
CA_CRT="${NGINX_DIR}/certs/basnas-ca.crt"

if [ ! -f "$CA_CRT" ] || [ ! -f "$CA_KEY" ]; then
  echo "Missing CA — run setup-admin-basnas-nginx.sh first." >&2
  exit 1
fi

mkdir -p "$CERT_DIR"
openssl genrsa -out "$CERT_DIR/privkey.pem" 2048

cat > /tmp/basnas-openssl.cnf <<'EOF'
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
DNS.2 = admin.basnas
DNS.3 = airflow.basnas
DNS.4 = immich.basnas
DNS.5 = kafka.basnas
DNS.6 = jobhunter.basnas
DNS.7 = radarr.basnas
DNS.8 = nzbget.basnas
DNS.9 = qbittorrent.basnas
DNS.10 = homebridge.basnas
DNS.11 = plex.basnas
DNS.12 = adguard.basnas
EOF

openssl req -new -key "$CERT_DIR/privkey.pem" -out /tmp/basnas.csr -config /tmp/basnas-openssl.cnf
openssl x509 -req -in /tmp/basnas.csr -CA "$CA_CRT" -CAkey "$CA_KEY" -CAcreateserial \
  -out "$CERT_DIR/cert.pem" -days 825 -sha256 -extfile /tmp/basnas-openssl.cnf -extensions ext
cat "$CERT_DIR/cert.pem" "$CA_CRT" > "$CERT_DIR/fullchain.pem"

echo "Re-issued leaf cert SANs:"
openssl x509 -in "$CERT_DIR/cert.pem" -noout -ext subjectAltName

DOCKER="${DOCKER:-/share/CACHEDEV1_DATA/.qpkg/container-station/bin/docker}"
$DOCKER exec nginx-office-c2h nginx -t
$DOCKER exec nginx-office-c2h nginx -s reload
echo "Done."
