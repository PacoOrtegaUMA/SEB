@echo off
REM Lanzar este propio script en una ventana MAXIMIZADA y terminar este proceso

start "" /MAX cmd /c "%~f0 run"
exit /b


:run
REM ===== Aquí empieza lo que realmente se ejecuta =====

rem Ver reglas de la cadena OUTPUT en la VM
set "HOST=localhost"
set "PORT=2222"
set "USER=profesor"
set "KEY=%~dp0Clave_Profesor_VM"
set "SCRIPT=%~f0"

if not exist "%KEY%" (
    echo ERROR: No se encuentra la clave privada: "%KEY%"
    echo.
    echo Pulsa una tecla para cerrar...
    pause >nul
    exit /b 1
)

set "SSHO= -o BatchMode=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL"

echo Mostrando reglas de la cadena OUTPUT...
ssh -i "%KEY%" -p %PORT% %SSHO% %USER%@%HOST% "sudo /usr/sbin/iptables -L OUTPUT -v -n --line-numbers"

set "EXITCODE=%ERRORLEVEL%"
echo.
echo EXITCODE SSH: %EXITCODE%
echo.

echo Borrando clave privada...
del /f /q "%KEY%"

echo Autodestruyendo script...
start "" /min cmd /c del "%SCRIPT%"

echo.
echo Pulsa una tecla para cerrar...
pause >nul

exit /b %EXITCODE%
