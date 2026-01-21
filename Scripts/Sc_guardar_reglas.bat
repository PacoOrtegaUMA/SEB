@echo off
rem Guardar reglas IPv4 e IPv6 en /etc/iptables/rules.v4 y /etc/iptables/rules.v6

set HOST=localhost
set PORT=2222
set USER=profesor

set KEY=%~dp0Clave_Profesor_VM

if not exist "%KEY%" (
    echo ERROR: No se encuentra la clave privada: %KEY%
    pause
    exit /b 1
)
set SSHOPTS= -o BatchMode=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL

echo Guardando reglas IPv4 e IPv6 en /etc/iptables/rules.v4 y rules.v6 ...
ssh -i "%KEY%" -p %PORT% %SSHOPTS%  %USER%@%HOST% "sudo /bin/sh -c '/usr/sbin/iptables-save > /etc/iptables/rules.v4 && /usr/sbin/ip6tables-save > /etc/iptables/rules.v6'"

echo EXITCODE SSH: %ERRORLEVEL%

if exist "%KEY%" (
    echo Borrando clave privada...
    del /f /q "%KEY%"
)


echo Autodestruyendo script...
start "" /min cmd /c del "%SCRIPT%"

exit /b %ERRORLEVEL%
