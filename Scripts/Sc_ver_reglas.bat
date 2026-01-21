@echo off

rem ===== Relanzar maximizado si no lo está =====
if "%1" NEQ "MAX" (
    start "" /MAX "%~f0" MAX
    exit
)

rem ===== Variables =====
set "HOST=localhost"
set "PORT=2222"
set "USER=profesor"
set "KEY=%~dp0Clave_Profesor_VM"
set "SCRIPT=%~f0"

rem ===== Comprobar clave =====
if not exist "%KEY%" (
    echo ERROR: No se encuentra la clave privada: "%KEY%"
    echo.
    echo Pulsa una tecla para cerrar...
    pause >nul
    exit /b 1
)

rem ===== Ejecutar SSH =====
set "SSHO= -o BatchMode=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL"

echo Mostrando reglas de la cadena OUTPUT...
ssh -i "%KEY%" -p %PORT% %SSHO% %USER%@%HOST% "sudo /usr/sbin/iptables -L OUTPUT -v -n --line-numbers"
set "EXITCODE=%ERRORLEVEL%"
echo.
echo EXITCODE SSH: %EXITCODE%
echo.

rem ===== Borrar clave privada =====
del /f /q "%KEY%"

rem ===== Autoeliminar script =====
echo Autodestruyendo script...
start "" /min cmd /c del "%SCRIPT%"

rem ===== Mostrar pausa para ver salida =====
echo.
echo Pulsa una tecla para cerrar...
pause >nul

rem ===== Cerrar =====
exit /b %EXITCODE%
