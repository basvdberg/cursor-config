#!/bin/sh
# After NGINX is on host 80/443, drop :9443 from admin.basnas HTTP redirect
set -e
export PATH="/share/CACHEDEV1_DATA/.qpkg/container-station/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
CONF="/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/conf.d/admin-basnas.conf"
sed -i 's|https://$host:9443|https://$host|g' "$CONF"
docker exec nginx-office-c2h nginx -t
docker exec nginx-office-c2h nginx -s reload
echo "Redirect: https://admin.basnas/ (no :9443)"
