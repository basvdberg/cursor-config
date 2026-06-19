#!/bin/sh
for u in http://192.168.2.2:8080/ http://10.0.5.1:8080/ http://127.0.0.1:8080/ https://192.168.2.2/; do
  printf "%s -> " "$u"
  curl -sk -o /dev/null -w "%{http_code}\n" --connect-timeout 3 "$u" || echo fail
done
