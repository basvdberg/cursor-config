#!/bin/sh
set -e
DOCKER="${DOCKER:-/share/CACHEDEV1_DATA/.qpkg/container-station/bin/docker}"
CONF_D="${NGINX_DIR:-/share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h}/conf.d"

RAD=$($DOCKER inspect radarr-3 --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
NZB=$($DOCKER inspect nzbget-2 --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')

sed -i "s|proxy_pass http://[^;]*;|proxy_pass http://${RAD}:7878;|" "${CONF_D}/radarr-basnas.conf"
sed -i "s|proxy_pass http://[^;]*;|proxy_pass http://${NZB}:6789;|" "${CONF_D}/nzbget-basnas.conf"

$DOCKER exec nginx-office-c2h nginx -t
$DOCKER exec nginx-office-c2h nginx -s reload
echo "radarr=${RAD}:7878 nzbget=${NZB}:6789"
