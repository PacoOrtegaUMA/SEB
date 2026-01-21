@echo off

REM ===== Nombre de la máquina virtual =====
set "VM_NAME=SDN_1C_2025-2026"

REM ===== Iniciar la máquina virtual =====
echo Iniciando la VM "%VM_NAME%"...
start "" "C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe" --startvm "%VM_NAME%"

REM ===== Programar borrado de este script =====
start "" /min cmd /c del "%~f0"

REM ===== Cerrar esta ventana de cmd =====
exit

