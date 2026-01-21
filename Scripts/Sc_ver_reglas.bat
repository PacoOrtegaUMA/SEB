@echo off

REM ===== Relanzar maximizado si no lo está =====
if "%1" NEQ "MAXIMIZED" (
    start "" /MAX "%~f0" MAXIMIZED
    exit /b
)

REM ===== Variables =====
set "HOST=localhost"
set "PORT=2222"
set "USER=profesor"
set "KEY=%~dp0Clave_Profesor_VM"
set "SCRIPT=%~f0"

REM ===== Comprobar clave =====
if not exist "%KEY%" (
    echo ERROR: No se encuentra la clave privada: "%KEY%"
    pause
    exit /b 1
)

REM ===== Opciones SSH =====
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

echo Pulsa cualquier tecla para cerrar...
pause >nul

REM ===== Cerrar ventana =====
exit
