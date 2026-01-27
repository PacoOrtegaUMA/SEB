@echo off

REM ===== Configuracion =====
set "VM_NAME=SDN_1C_2025-2026"
set "SNAP_NAME=InicioCurso"
set "VBOXM=C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

REM ===== Apagar VM si esta encendida =====
"%VBOXM%" controlvm "%VM_NAME%" poweroff 2>nul

REM ===== Esperar un poco =====
timeout /t 3 /nobreak >nul

REM ===== Restaurar snapshot =====
"%VBOXM%" snapshot "%VM_NAME%" restore "%SNAP_NAME%" >nul 2>&1

REM ===== Arrancar VM =====
start "" "C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe" --startvm "%VM_NAME%"

REM ===== Autodestruir script =====
start "" /min cmd /c del "%~f0"

REM ===== Cerrar ventana =====
exit
