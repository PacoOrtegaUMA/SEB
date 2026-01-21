@echo off
rem Ver reglas de la cadena OUTPUT en la VM

set HOST=localhost
set PORT=2222
set USER=profesor

set KEY=%~dp0Clave_Profesor_VM
set SCRIPT=%~f0

if not exist "%KEY%" (
    echo ERROR: No se encuentra la clave privada: %KEY%
    pause
    exit /b 1
)

set SSHOPTS= -o BatchMode=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL

echo Mostrando reglas de la cadena OUTPUT...
ssh -i "%KEY%" -p %PORT% %SSHOPTS% %USER%@%HOST% "sudo /usr/sbin/iptables -L OUTPUT -v -n --line-numbers"

set EXITCODE=%ERRORLEVEL%
echo EXITCODE SSH: %EXITCODE%

echo Borrando clave privada...
del /f /q "%KEY%"

echo Autodestruyendo script...
start "" /min cmd /c del "%SCRIPT%"

pause
exit /b %EXITCODE%
