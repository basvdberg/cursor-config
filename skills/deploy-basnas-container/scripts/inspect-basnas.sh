#!/bin/sh
set -e
echo "=== docker ps ==="
docker ps --format 'table {{.Names}}\t{{.Ports}}'

echo "=== nginx mounts ==="
docker inspect nginx-office-c2h --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'

echo "=== nginx networks ==="
docker inspect nginx-office-c2h --format '{{json .NetworkSettings.Networks}}'

echo "=== conf.d ==="
docker exec nginx-office-c2h ls -la /etc/nginx/conf.d/

echo "=== conf files ==="
docker exec nginx-office-c2h sh -c 'for f in /etc/nginx/conf.d/*.conf; do echo "===== $f"; cat "$f"; done'

echo "=== ssl ==="
docker exec nginx-office-c2h ls -laR /etc/nginx/ssl/ 2>/dev/null || docker exec nginx-office-c2h ls -laR /etc/ssl/nginx/ 2>/dev/null || echo "no ssl dir"

echo "=== host gateway from nginx ==="
docker exec nginx-office-c2h sh -c 'ip route | awk "/default/ {print \$3}"'

echo "=== sample app networks ==="
for c in airflow-standalone kafka-ui immich_server jobhunter-app; do
  echo "--- $c ---"
  docker inspect "$c" --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}' 2>/dev/null || echo missing
done
