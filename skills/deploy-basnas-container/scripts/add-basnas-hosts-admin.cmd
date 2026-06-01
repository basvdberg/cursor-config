@echo off
:: Run as Administrator (right-click -> Run as administrator)
set HOSTS=%SystemRoot%\System32\drivers\etc\hosts
findstr /i "admin.basnas" %HOSTS% >nul && (
  echo admin.basnas already in hosts file.
  goto :done
)
echo.>>%HOSTS%
echo # BasNAS internal zone>>%HOSTS%
echo 192.168.2.2 admin.basnas airflow.basnas immich.basnas kafka.basnas jobhunter.basnas>>%HOSTS%
echo Added *.basnas entries pointing to 192.168.2.2
:done
ipconfig /flushdns
nslookup admin.basnas
pause
