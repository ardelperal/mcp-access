@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   🔄 MIGRACIÓN A MCP ACCESS CENTRALIZADO
echo ========================================
echo.

REM Verificar que el MCP centralizado esté instalado
if not exist "C:\MCPs\MCP_ACCESS\src\mcp_access_server.py" (
    echo ❌ Error: MCP Access centralizado no encontrado en C:\MCPs\MCP_ACCESS
    echo.
    echo 📥 Primero instala el MCP centralmente:
    echo curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/install-mcp-central.bat
    echo install-mcp-central.bat
    echo.
    pause
    exit /b 1
)

echo ✅ MCP Access centralizado encontrado en C:\MCPs\MCP_ACCESS
echo.

REM Detectar configuración actual
echo 🔍 Detectando configuración actual...
echo.

set "OLD_CONFIG_FOUND=false"
set "SUBMODULE_FOUND=false"
set "LOCAL_INSTALL_FOUND=false"

REM Verificar submodules
git submodule status 2>nul | findstr "mcp-access" >nul
if !errorlevel! equ 0 (
    set "SUBMODULE_FOUND=true"
    echo 📁 Detectado: Git submodule de mcp-access
)

REM Verificar instalación local
if exist "mcp-access" (
    set "LOCAL_INSTALL_FOUND=true"
    echo 📁 Detectado: Instalación local en carpeta mcp-access
)

if exist "mcp-modules\mcp-access" (
    set "LOCAL_INSTALL_FOUND=true"
    echo 📁 Detectado: Instalación local en mcp-modules\mcp-access
)

REM Verificar configuraciones existentes
if exist "mcp.json" (
    set "OLD_CONFIG_FOUND=true"
    echo 📄 Detectado: Archivo mcp.json
)

if exist "claude_desktop_config.json" (
    set "OLD_CONFIG_FOUND=true"
    echo 📄 Detectado: Archivo claude_desktop_config.json
)

echo.

REM Crear backup de configuraciones existentes
if "!OLD_CONFIG_FOUND!"=="true" (
    echo 💾 Creando backup de configuraciones existentes...
    if exist "mcp.json" (
        copy "mcp.json" "mcp.json.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul
        echo    ✅ mcp.json → mcp.json.backup
    )
    if exist "claude_desktop_config.json" (
        copy "claude_desktop_config.json" "claude_desktop_config.json.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul
        echo    ✅ claude_desktop_config.json → claude_desktop_config.json.backup
    )
    echo.
)

REM Limpiar instalaciones locales
if "!SUBMODULE_FOUND!"=="true" (
    echo 🧹 Eliminando git submodule...
    git submodule deinit -f mcp-modules/mcp-access 2>nul
    git rm -f mcp-modules/mcp-access 2>nul
    if exist ".git\modules\mcp-modules\mcp-access" (
        rmdir /s /q ".git\modules\mcp-modules\mcp-access" 2>nul
    )
    echo    ✅ Submodule eliminado
    echo.
)

if "!LOCAL_INSTALL_FOUND!"=="true" (
    echo 🧹 Eliminando instalación local...
    if exist "mcp-access" (
        rmdir /s /q "mcp-access" 2>nul
        echo    ✅ Carpeta mcp-access eliminada
    )
    if exist "mcp-modules\mcp-access" (
        rmdir /s /q "mcp-modules\mcp-access" 2>nul
        echo    ✅ Carpeta mcp-modules\mcp-access eliminada
    )
    echo.
)

REM Crear nueva configuración centralizada
echo 🔧 Creando nueva configuración centralizada...

(
echo {
echo   "mcpServers": {
echo     "mcp-access": {
echo       "command": "python",
echo       "args": ["C:/MCPs/MCP_ACCESS/src/mcp_access_server.py"],
echo       "env": {
echo         "PYTHONPATH": "C:/MCPs/MCP_ACCESS/src"
echo       }
echo     }
echo   }
echo }
) > mcp.json

echo ✅ Archivo mcp.json creado con configuración centralizada
echo.

REM Verificar dependencias del proyecto
echo 🔍 Verificando dependencias del proyecto...
if exist "requirements.txt" (
    findstr /i "pyodbc" requirements.txt >nul
    if !errorlevel! neq 0 (
        echo 📦 Añadiendo pyodbc a requirements.txt...
        echo pyodbc>>requirements.txt
        echo    ✅ pyodbc añadido a requirements.txt
    ) else (
        echo    ✅ pyodbc ya está en requirements.txt
    )
) else (
    echo 📦 Creando requirements.txt con pyodbc...
    echo pyodbc>requirements.txt
    echo    ✅ requirements.txt creado
)

echo.

REM Instalar dependencias si es necesario
python -c "import pyodbc" 2>nul
if !errorlevel! neq 0 (
    echo 📦 Instalando pyodbc...
    pip install pyodbc
    if !errorlevel! equ 0 (
        echo    ✅ pyodbc instalado correctamente
    ) else (
        echo    ⚠️ Error instalando pyodbc, instálalo manualmente: pip install pyodbc
    )
) else (
    echo ✅ pyodbc ya está instalado
)

echo.
echo ========================================
echo   ✅ MIGRACIÓN COMPLETADA
echo ========================================
echo.
echo 🎯 Tu proyecto ahora usa el MCP Access centralizado
echo 📍 Ubicación: C:\MCPs\MCP_ACCESS
echo 📄 Configuración: mcp.json (en este directorio)
echo.
echo 🚀 Próximos pasos:
echo 1. Reinicia Trae AI para que cargue la nueva configuración
echo 2. Verifica que el MCP funciona correctamente
echo 3. Los backups de tu configuración anterior están guardados
echo.
echo 💡 Si tienes problemas, revisa los archivos .backup creados
echo.
pause