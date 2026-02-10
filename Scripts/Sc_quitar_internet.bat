@echo on
rem Quitar internet al usuario UID 1000 dentro de la VM

setlocal

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


echo === Ejecutando SSH ===
ssh -i "%KEY%" -p %PORT% %SSHOPTS% %USER%@%HOST% "sudo /usr/sbin/iptables -D OUTPUT -m owner --uid-owner 1000 -p tcp -m multiport --dports 80,443 -j ACCEPT 2>/dev/null || true"
ssh -i "%KEY%" -p %PORT% %SSHOPTS% %USER%@%HOST% "sudo /usr/sbin/iptables -D OUTPUT -m owner --uid-owner 1000 -p tcp --dport 3128 -j ACCEPT 2>/dev/null || true"
echo === EXITCODE SSH: %ERRORLEVEL% ===


if exist "%KEY%" (
    echo Borrando clave privada...
    del /f /q "%KEY%"
)


echo Autodestruyendo script...
start /b "" cmd /c del /f /q "%~f0" & exit


