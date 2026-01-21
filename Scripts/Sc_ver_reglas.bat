@echo off
REM ==============================
REM Maximizar Esta Ventana y Continuar
REM ==============================
setlocal

REM Si no tiene el marcador MAX, relanzar maximizado y CERRAR la original
if "%1" NEQ "MAX" (
    start "" /MAX "%~f0" MAX
    exit /b
)

REM ==============================
REM Variables SSH
REM ==============================
set "HOST=localhost"
set "PORT=2222"
set "USER=profesor"
set "KEY=%~dp0Clave_Profesor_VM"
set "THISBAT=%~f0"

REM ==============================
REM Comprobar clave
REM ==============================
if not exist "%KEY%" (
    echo ERROR: No se encuentra la clave privada: "%KEY%"
    echo.
    echo Pulsa una tecla para cerrar...
    pause >nul
    exit /b 1
)

REM ==============================
REM Ejecutar SSH
REM ==============================
set "SSHO= -o BatchMode=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL"

echo Mostrando reglas de la cadena OUTPUT...
ssh -i "%KEY%" -p %PORT% %SSHO% %USER%@%HOST% "sudo /usr/sbin/iptables -L OUTPUT -v -n --line-numbers"

set "EXITCODE=%ERRORLEVEL%"

echo.
echo EXITCODE SSH: %EXITCODE%
echo.

REM ==============================
REM Borrar clave privada
REM ==============================
if exist "%KEY%" (
    echo Borrando clave privada...
    del /f /q "%KEY%"
)

REM ==============================
REM Auto-eliminacion y Cierre Limpio
REM ==============================
echo Limpiando rastro y saliendo...

REM El truco (goto) 2>nul libera el archivo para que pueda ser borrado 
REM mientras cmd.exe ejecuta el comando independiente de borrado.
(goto) 2>nul & start /b "" cmd /c "del /f /q "%THISBAT%"" & exit /b %EXITCODE%
