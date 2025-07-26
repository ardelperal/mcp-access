@echo off
echo ========================================
echo   Configurador de MCP Access en Claude
echo ========================================
echo.

set "CONFIG_FILE=%APPDATA%\Claude\claude_desktop_config.json"
set "BACKUP_FILE=%APPDATA%\Claude\claude_desktop_config.json.backup"

echo Verificando configuracion de Claude Desktop...

if not exist "%CONFIG_FILE%" (
    echo ERROR: No se encontro el archivo de configuracion de Claude Desktop
    echo Ubicacion esperada: %CONFIG_FILE%
    echo.
    echo Asegurate de que Claude Desktop este instalado y configurado.
    pause
    exit /b 1
)

echo Creando backup de la configuracion actual...
copy "%CONFIG_FILE%" "%BACKUP_FILE%" >nul

echo.
echo Configuracion actual de MCPs:
echo ==============================
type "%CONFIG_FILE%"
echo.
echo ==============================

echo.
echo INSTRUCCIONES PARA AGREGAR MCP ACCESS:
echo.
echo 1. Abre el archivo: %CONFIG_FILE%
echo 2. Agrega esta seccion dentro de "mcpServers":
echo.
echo     "access-db": {
echo       "command": "python",
echo       "args": [
echo         "c:\\Users\\adm1\\Desktop\\Proyectos\\mcp-access\\src\\mcp_access_server.py"
echo       ],
echo       "env": {
echo         "PYTHONPATH": "c:\\Users\\adm1\\Desktop\\Proyectos\\mcp-access\\src"
echo       }
echo     }
echo.
echo 3. Asegurate de agregar una coma despues del ultimo MCP existente
echo 4. Guarda el archivo y reinicia Claude Desktop
echo.
echo BACKUP creado en: %BACKUP_FILE%
echo.

pause

echo.
echo ¿Quieres abrir el archivo de configuracion para editarlo? (S/N)
set /p "choice=Respuesta: "

if /i "%choice%"=="S" (
    echo Abriendo archivo de configuracion...
    notepad "%CONFIG_FILE%"
) else (
    echo Configuracion manual requerida.
)

echo.
echo Proceso completado. Reinicia Claude Desktop para aplicar los cambios.
pause