@echo off
rem Subir policies.json y cerrar Firefox del usuario dentro de la VM

set HOST=localhost
set PORT=2222
set USER=profesor

rem Clave privada
set KEY=%~dp0Clave_Profesor_VM

rem Archivo local y remoto
set LOCAL_JSON=%~dp0policies.json
set REMOTE_FILE=/etc/firefox/policies/policies.json


rem Comprobar clave
if not exist "%KEY%" (
    echo ERROR: No se encuentra la clave privada: %KEY%
    pause
    exit /b 1
)

rem Comprobar policies.json
if not exist "%LOCAL_JSON%" (
    echo ERROR: No se encuentra policies.json en la carpeta del script
    pause
    exit /b 1
)


set SSHOPTS= -o BatchMode=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL


echo Subiendo policies.json a la VM...
scp -i "%KEY%" -P %PORT% "%LOCAL_JSON%" %USER%@%HOST%:%REMOTE_FILE%
if errorlevel 1 (
    echo ERROR al copiar policies.json con scp
    pause
    exit /b 1
)


echo Cerrando Firefox del usuario alumno...
ssh -i "%KEY%" -p %PORT% %SSHOPTS% %USER%@%HOST% "sudo /usr/bin/pkill -u usuario firefox 2>/dev/null || true"


echo EXITCODE SSH: %ERRORLEVEL%


rem Borrar clave privada
if exist "%KEY%" (
    echo Borrando clave privada...
    del /f /q "%KEY%"
)

rem Borrar policies.json local
if exist "%LOCAL_JSON%" (
    echo Borrando policies.json local...
    del /f /q "%LOCAL_JSON%"
)


echo Autodestruyendo script...
start "" /min cmd /c del "%~f0"


exit /b %ERRORLEVEL%
