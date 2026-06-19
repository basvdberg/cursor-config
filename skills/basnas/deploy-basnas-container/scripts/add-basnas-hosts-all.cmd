@echo off
:: Run as Administrator — adds all *.basnas hostnames to the Windows hosts file
set HOSTS=%SystemRoot%\System32\drivers\etc\hosts
set LINE=192.168.2.2 admin.basnas airflow.basnas immich.basnas radarr.basnas nzbget.basnas qbittorrent.basnas homebridge.basnas plex.basnas adguard.basnas
findstr /i "admin.basnas" %HOSTS% >nul && (
  echo BasNAS hosts block already present. Edit %HOSTS% manually if you need more names.
  goto :flush
)
echo.>>%HOSTS%
echo # BasNAS internal zone>>%HOSTS%
echo %LINE%>>%HOSTS%
echo Added BasNAS hostnames pointing to 192.168.2.2
:flush
ipconfig /flushdns
echo.
echo Test: ping admin.basnas
ping -n 1 admin.basnas
pause
