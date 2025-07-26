@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    CONFIGURACION MCP ACCESS DATABASE
echo    Con deteccion automatica de proxy
echo ========================================
echo.

REM Verificar Python
echo [INFO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instale Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% encontrado

REM Verificar Git
echo [INFO] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git no encontrado. Instale Git desde https://git-scm.com
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('git --version 2^>^&1') do set GIT_VERSION=%%i
echo [OK] %GIT_VERSION% encontrado

echo.
echo ========================================
echo    DETECCION AUTOMATICA DE PROXY
echo ========================================

REM Ejecutar detección de proxy
echo [INFO] Detectando configuracion de proxy...
python detect_proxy.py

echo.
echo ========================================
echo    OPCIONES DE CONFIGURACION
echo ========================================
echo.
echo 1. Configuracion global (recomendado)
echo 2. Configuracion local (solo este proyecto)
echo 3. Verificar instalacion existente
echo 4. Solo detectar proxy (sin configurar MCP)
echo.
set /p OPTION="Seleccione una opcion (1-4): "

if "%OPTION%"=="1" goto GLOBAL_CONFIG
if "%OPTION%"=="2" goto LOCAL_CONFIG
if "%OPTION%"=="3" goto VERIFY_CONFIG
if "%OPTION%"=="4" goto PROXY_ONLY
echo [ERROR] Opcion invalida
pause
exit /b 1

:PROXY_ONLY
echo.
echo [INFO] Deteccion de proxy completada
echo [INFO] No se realizara configuracion de MCP
pause
exit /b 0

:GLOBAL_CONFIG
echo.
echo [INFO] Configurando MCP globalmente...
set MCP_DIR=%USERPROFILE%\.mcp\servers\mcp-access
goto SETUP_MCP

:LOCAL_CONFIG
echo.
echo [INFO] Configurando MCP localmente...
set MCP_DIR=%CD%\.mcp\servers\mcp-access
goto SETUP_MCP

:SETUP_MCP
echo [INFO] Directorio MCP: %MCP_DIR%

REM Crear directorios
if not exist "%MCP_DIR%" mkdir "%MCP_DIR%"

REM Sincronizar repositorio
echo [INFO] Sincronizando repositorio...
if exist "%MCP_DIR%\.git" (
    echo [INFO] Actualizando repositorio existente...
    cd /d "%MCP_DIR%"
    git fetch origin
    git reset --hard origin/main
) else (
    echo [INFO] Clonando repositorio...
    if exist "%MCP_DIR%" rmdir /s /q "%MCP_DIR%"
    git clone https://github.com/ardelperal/mcp-access.git "%MCP_DIR%"
)

if errorlevel 1 (
    echo [ERROR] Error sincronizando repositorio
    pause
    exit /b 1
)

echo [OK] Repositorio sincronizado

REM Instalar dependencias
echo [INFO] Instalando dependencias...
cd /d "%MCP_DIR%"
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Error instalando dependencias
    echo [INFO] Verifique la configuracion de proxy si esta en una red corporativa
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas

REM Configurar MCP
echo [INFO] Configurando MCP...
python auto_setup.py https://github.com/ardelperal/mcp-access.git

if errorlevel 1 (
    echo [ERROR] Error configurando MCP
    pause
    exit /b 1
)

echo [OK] MCP configurado

goto FINISH

:VERIFY_CONFIG
echo.
echo [INFO] Verificando instalacion existente...

REM Verificar directorio global
set GLOBAL_MCP=%USERPROFILE%\.mcp\servers\mcp-access
if exist "%GLOBAL_MCP%" (
    echo [OK] Instalacion global encontrada: %GLOBAL_MCP%
    cd /d "%GLOBAL_MCP%"
    python src\mcp_access_server.py --version 2>nul
    if errorlevel 1 (
        echo [WARNING] MCP global no responde correctamente
    ) else (
        echo [OK] MCP global funcionando
    )
) else (
    echo [INFO] No se encontro instalacion global
)

REM Verificar directorio local
set LOCAL_MCP=%CD%\.mcp\servers\mcp-access
if exist "%LOCAL_MCP%" (
    echo [OK] Instalacion local encontrada: %LOCAL_MCP%
    cd /d "%LOCAL_MCP%"
    python src\mcp_access_server.py --version 2>nul
    if errorlevel 1 (
        echo [WARNING] MCP local no responde correctamente
    ) else (
        echo [OK] MCP local funcionando
    )
) else (
    echo [INFO] No se encontro instalacion local
)

goto FINISH

:FINISH
echo.
echo ========================================
echo    CONFIGURACION COMPLETADA
echo ========================================
echo.
echo [INFO] MCP Access Database configurado exitosamente
echo [INFO] Reinicie Trae 2.0 para aplicar los cambios
echo.
echo Archivos de configuracion:
if exist "%USERPROFILE%\.mcp\config.json" echo   - Global: %USERPROFILE%\.mcp\config.json
if exist "%CD%\.mcp\config.json" echo   - Local: %CD%\.mcp\config.json
echo.
echo Para probar el MCP:
echo   1. Reinicie Trae 2.0
echo   2. Abra un archivo .accdb
echo   3. Use comandos como "mostrar tablas" o "consultar datos"
echo.
echo ========================================
pause