#!/bin/sh
# Register *.basnas on QNAP system dnsmasq (listens on LAN br0).
# Requires admin: run with sudo on BasNAS.
set -e

BASNAS_IP="${BASNAS_IP:-192.168.2.2}"
CONF="/share/CACHEDEV1_DATA/homes/bas/dns-basnas.dnsmasq"
HOSTS="/share/CACHEDEV1_DATA/homes/bas/basnas-hosts"
SYS_HOSTS="/etc/hosts"

cat > "$CONF" <<EOF
# BasNAS internal DNS zone (managed by deploy-basnas-container skill)
address=/.basnas/${BASNAS_IP}
address=/admin.basnas/${BASNAS_IP}
address=/airflow.basnas/${BASNAS_IP}
address=/immich.basnas/${BASNAS_IP}
address=/plex.basnas/${BASNAS_IP}
address=/radarr.basnas/${BASNAS_IP}
address=/nzbget.basnas/${BASNAS_IP}
address=/qbittorrent.basnas/${BASNAS_IP}
address=/homebridge.basnas/${BASNAS_IP}
EOF

cat > "$HOSTS" <<EOF
${BASNAS_IP} admin.basnas
${BASNAS_IP} airflow.basnas
${BASNAS_IP} immich.basnas
${BASNAS_IP} plex.basnas
${BASNAS_IP} radarr.basnas
${BASNAS_IP} nzbget.basnas
${BASNAS_IP} qbittorrent.basnas
${BASNAS_IP} homebridge.basnas
EOF

if ! grep -q 'dns-basnas.dnsmasq' /etc/dnsmasq.conf 2>/dev/null; then
  echo "conf-file=$CONF" >> /etc/dnsmasq.conf
  echo "addn-hosts=$HOSTS" >> /etc/dnsmasq.conf
fi

# Ensure QNAP's main listen-address includes BASNAS_IP
if grep -q '^listen-address' /etc/dnsmasq.conf 2>/dev/null; then
  CURRENT="$(grep '^listen-address' /etc/dnsmasq.conf | head -1)"
  if ! echo "$CURRENT" | grep -q "$BASNAS_IP"; then
    UPDATED="${CURRENT},${BASNAS_IP}"
    sed -i "s|^listen-address.*|$UPDATED|" /etc/dnsmasq.conf
  fi
else
  echo "listen-address=${BASNAS_IP}" >> /etc/dnsmasq.conf
fi

# QNAP dnsmasq reliably reads /etc/hosts; keep a managed basnas block there
if [ -f "$SYS_HOSTS" ]; then
  cp "$SYS_HOSTS" "${SYS_HOSTS}.bak.basnas.$(date +%s)"
  awk '
    BEGIN{skip=0}
    /# BEGIN BASNAS LOCAL DNS/{skip=1; next}
    /# END BASNAS LOCAL DNS/{skip=0; next}
    skip==0 {print}
  ' "$SYS_HOSTS" > /tmp/hosts.nobasnas
  {
    cat /tmp/hosts.nobasnas
    echo "# BEGIN BASNAS LOCAL DNS"
    cat "$HOSTS"
    echo "# END BASNAS LOCAL DNS"
  } > "$SYS_HOSTS"
fi

# Reload QNAP dnsmasq
if [ -x /etc/init.d/dnsmasq.sh ]; then
  /etc/init.d/dnsmasq.sh restart
elif killall -HUP dnsmasq 2>/dev/null; then
  echo "Sent HUP to dnsmasq"
else
  killall dnsmasq 2>/dev/null || true
  sleep 1
  /sbin/dnsmasq &
fi

sleep 2
echo "Testing admin.basnas via 127.0.1.1 and ${BASNAS_IP}..."
nslookup admin.basnas 127.0.1.1 || true
nslookup admin.basnas "${BASNAS_IP}" || true
echo "Done. Point router DHCP DNS to ${BASNAS_IP} OR keep router and add NRPT/hosts on clients."
