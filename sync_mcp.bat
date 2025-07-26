@echo off
REM sync_mcp.bat - Script de sincronización para Windows

setlocal enabledelayedexpansion

REM Configuración
set "REPO_URL=https://github.com/TU_USUARIO/mcp-access-database.git"
set "MCP_DIR=%USERPROFILE%\.mcp\servers\mcp-access"
set "CONFIG_FILE=%USERPROFILE%\.mcp\config.json"

echo ========================================
echo   MCP Access Database - Sincronización
echo ========================================
echo.

REM Verificar si Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git no está instalado. Por favor instala Git primero.
    pause
    exit /b 1
)

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado. Por favor instala Python 3.8+ primero.
    pause
    exit /b 1
)

echo [1/5] Preparando directorios...
if not exist "%USERPROFILE%\.mcp\servers" (
    mkdir "%USERPROFILE%\.mcp\servers"
)

echo [2/5] Sincronizando repositorio...
if exist "%MCP_DIR%\.git" (
    echo Actualizando repositorio existente...
    cd /d "%MCP_DIR%"
    git fetch origin
    git reset --hard origin/main
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo actualizar el repositorio
        pause
        exit /b 1
    )
    echo Repositorio actualizado
) else (
    echo Clonando repositorio...
    if exist "%MCP_DIR%" (
        rmdir /s /q "%MCP_DIR%"
    )
    git clone "%REPO_URL%" "%MCP_DIR%"
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo clonar el repositorio
        echo Verifica que la URL sea correcta: %REPO_URL%
        pause
        exit /b 1
    )
    echo Repositorio clonado
)

echo [3/5] Instalando dependencias...
cd /d "%MCP_DIR%"
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo [4/5] Configurando MCP...
if not exist "%CONFIG_FILE%" (
    if not exist "%USERPROFILE%\.mcp" (
        mkdir "%USERPROFILE%\.mcp"
    )
    echo {"mcpServers": {}} > "%CONFIG_FILE%"
)

REM Crear configuración temporal
set "TEMP_CONFIG=%TEMP%\mcp_access_config.json"
(
echo {
echo   "mcpServers": {
echo     "access-db": {
echo       "command": "python",
echo       "args": [
echo         "%MCP_DIR:\=\\%\\src\\mcp_access_server.py"
echo       ],
echo       "env": {
echo         "PYTHONPATH": "%MCP_DIR:\=\\%\\src",
echo         "MCP_ACCESS_LOG_LEVEL": "INFO"
echo       },
echo       "description": "Microsoft Access Database MCP Server"
echo     }
echo   }
echo }
) > "%TEMP_CONFIG%"

REM Copiar configuración (método simple)
copy "%TEMP_CONFIG%" "%CONFIG_FILE%" >nul
del "%TEMP_CONFIG%"

echo [5/5] Verificando instalación...
python src\mcp_access_server.py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ADVERTENCIA: No se pudo verificar el MCP
) else (
    echo ✅ MCP verificado correctamente
)

echo.
echo ========================================
echo   🎉 Sincronización completada!
echo ========================================
echo.
echo MCP instalado en: %MCP_DIR%
echo Configuración en: %CONFIG_FILE%
echo.
echo Para usar en Trae 2.0, reinicia la aplicación.
echo.
echo COMANDOS ÚTILES:
echo - Actualizar: sync_mcp.bat
echo - Probar: cd "%MCP_DIR%" ^&^& start.bat
echo.
pause