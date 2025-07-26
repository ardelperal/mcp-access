@echo off
REM quick_setup.bat - Configuración rápida multiplataforma

echo ========================================
echo   MCP Access Database - Setup Rápido
echo ========================================
echo.

REM Detectar si estamos en un entorno con Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python detectado
    set "PYTHON_CMD=python"
    goto :python_setup
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python3 detectado
    set "PYTHON_CMD=python3"
    goto :python_setup
)

echo ❌ Python no encontrado
echo Por favor instala Python 3.8+ desde https://python.org
pause
exit /b 1

:python_setup
echo.
echo Selecciona el método de sincronización:
echo.
echo [1] GitHub Repository (Recomendado)
echo [2] Configuración Local
echo [3] Cloud Storage (Manual)
echo.
set /p choice="Elige una opción (1-3): "

if "%choice%"=="1" goto :github_setup
if "%choice%"=="2" goto :local_setup
if "%choice%"=="3" goto :cloud_setup

echo Opción inválida
pause
exit /b 1

:github_setup
echo.
set /p repo_url="Ingresa la URL del repositorio GitHub: "
if "%repo_url%"=="" (
    echo URL requerida
    pause
    exit /b 1
)

echo Configurando desde GitHub...
%PYTHON_CMD% auto_setup.py "%repo_url%"
goto :end

:local_setup
echo.
echo Configurando instalación local...
if exist "sync_mcp.bat" (
    call sync_mcp.bat
) else (
    echo sync_mcp.bat no encontrado
    echo Ejecutando configuración manual...
    %PYTHON_CMD% auto_setup.py .
)
goto :end

:cloud_setup
echo.
echo Configuración de Cloud Storage:
echo.
echo 1. Mueve la carpeta MCP a tu carpeta sincronizada (Dropbox/OneDrive/etc.)
echo 2. Crea un enlace simbólico:
echo    mklink /D "%%USERPROFILE%%\.mcp\servers\mcp-access" "RUTA_CLOUD\mcp-access"
echo 3. Actualiza la configuración en cada máquina
echo.
echo Consulta SYNC_GUIDE.md para instrucciones detalladas
pause
goto :end

:end
echo.
echo ========================================
echo   Configuración completada
echo ========================================
echo.
echo Próximos pasos:
echo 1. Reinicia Trae 2.0
echo 2. Verifica que el MCP aparezca en los logs
echo 3. Prueba con: "Conecta a una base de datos Access"
echo.
pause