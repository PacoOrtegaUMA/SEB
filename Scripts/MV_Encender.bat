@echo off
REM Nombre de la maquina virtual en VirtualBox
set "VM_NAME=SDN_1C_2025-2026"

echo Iniciando la maquina virtual "%VM_NAME%"...
"C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe" --startvm "%VM_NAME%"

REM Comprobar si hubo error
if errorlevel 1 (
    echo Error al iniciar la VM "%VM_NAME%".
    pause
    goto :EOF
)

echo VM iniciada correctamente.
echo Este script se auto-eliminara ahora.

REM Trucazo: lanzar otro cmd que borre este .bat cuando termine
start "" /min cmd /c del "%~f0"

REM Cerrar este cmd
exit

