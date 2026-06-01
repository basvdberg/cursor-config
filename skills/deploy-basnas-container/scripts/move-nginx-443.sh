#!/bin/sh
set -e

OLD="nginx-office-c2h-old"
NEW="nginx-office-c2h"

docker rm -f "$OLD" >/dev/null 2>&1 || true
docker rename "$NEW" "$OLD"

if docker run -d \
  --name "$NEW" \
  --restart unless-stopped \
  -p 80:80 \
  -p 443:443 \
  -v /share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/letsencrypt:/etc/letsencrypt \
  -v /share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/certs:/etc/nginx/certs \
  -v /share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/conf.d:/etc/nginx/conf.d \
  -v /share/CACHEDEV1_DATA/homes/bas/nginx-office-c2h/html:/var/www/html \
  nginx:alpine >/tmp/nginx_new_id.txt 2>/tmp/nginx_new_err.txt; then
  docker network connect broesliagent_default "$NEW" >/dev/null 2>&1 || true
  docker network connect immich_default "$NEW" >/dev/null 2>&1 || true
  docker network connect openclaw_default "$NEW" >/dev/null 2>&1 || true
  docker network connect jobhunter_default "$NEW" >/dev/null 2>&1 || true
  docker network connect kafka_default "$NEW" >/dev/null 2>&1 || true
  docker network connect apache-airflow_default "$NEW" >/dev/null 2>&1 || true
  docker exec "$NEW" nginx -t
  echo "MIGRATION_OK"
else
  echo "MIGRATION_FAILED"
  cat /tmp/nginx_new_err.txt
  docker rm -f "$NEW" >/dev/null 2>&1 || true
  docker rename "$OLD" "$NEW"
  exit 1
fi
