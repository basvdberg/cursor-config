#!/bin/sh
for c in radarr-3 nzbget-2 qbittorrent-1 homebridge-2 airflow-standalone; do
  echo -n "$c: "
  docker inspect "$c" --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}' 2>/dev/null || echo missing
done
