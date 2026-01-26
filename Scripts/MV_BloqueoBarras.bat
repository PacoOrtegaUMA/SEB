@echo off

REM ============================
REM Uso: bloquear_vbox_ui.bat NOMBRE_VM
REM ============================

if "%~1"=="" (
    echo Uso: %~nx0 NOMBRE_DE_LA_VM
    pause
    exit /b 1
)

set "VM=%~1"
set "VBOX=C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

echo Aplicando bloqueo a la VM: %VM%

REM Desactivar barra de estado
"%VBOX%" setextradata "%VM%" GUI/StatusBar/Enabled false

REM Desactivar barra de menus
"%VBOX%" setextradata "%VM%" GUI/MenuBar/Enabled false

echo Listo.
exit /b 0 