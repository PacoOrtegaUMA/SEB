@echo off

REM Ruta de la carpeta Descargas del usuario actual
set DOWNLOADS=%USERPROFILE%\Downloads

REM Borrar todos los archivos
del /f /q "%DOWNLOADS%\*.*" >nul 2>&1

REM Borrar todas las subcarpetas
for /d %%D in ("%DOWNLOADS%\*") do rmdir /s /q "%%D"

REM ===== Cerrar esta ventana de cmd =====
exit