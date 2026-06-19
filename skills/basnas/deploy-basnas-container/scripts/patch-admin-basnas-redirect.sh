#!/bin/sh
CONF="/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/conf.d/admin-basnas.conf"
# Until NGINX listens on host 443, HTTPS is on published port 9443
sed -i 's|return 301 https://\$host\$request_uri;|return 301 https://$host:9443$request_uri;|' "$CONF"
docker exec nginx-office-c2h nginx -t && docker exec nginx-office-c2h nginx -s reload
echo "Patched redirect to https://admin.basnas:9443/"
