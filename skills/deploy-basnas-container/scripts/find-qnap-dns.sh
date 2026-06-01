#!/bin/sh
find /etc -name '*dnsmasq*' 2>/dev/null
find /var -name '*dnsmasq*' 2>/dev/null | head -20
grep -r 'address=' /etc/config/ 2>/dev/null | head -10
ps w | grep -i dns
