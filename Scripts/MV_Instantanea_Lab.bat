@echo off

REM ===== Configuracion =====
if "%~1"=="" (
    echo Uso: %~nx0 NOMBRE_DE_LA_VM
    pause
    exit /b 1
)
set "VM_NAME=%~1"
set "SNAP_NAME=InicioCurso"
set "VBOXM=C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

REM ===== Apagar VM si esta encendida =====
"%VBOXM%" controlvm "%VM_NAME%" poweroff 2>nul

REM ===== Esperar un poco =====
timeout /t 3 /nobreak >nul

REM ===== Restaurar snapshot =====
"%VBOXM%" snapshot "%VM_NAME%" restore "%SNAP_NAME%" >nul 2>&1

exit

