@echo off
REM setup-mcp-access.bat - Script para integrar mcp-access en otro proyecto (Windows)

echo 🚀 Configurando MCP Access Database...

REM Verificar si es un repositorio git
if not exist ".git" (
    echo ❌ Error: Este directorio no es un repositorio git
    pause
    exit /b 1
)

REM Crear directorio para módulos MCP si no existe
if not exist "mcp-modules" mkdir mcp-modules

REM Añadir como submodule si no existe
if not exist "mcp-modules\mcp-access" (
    echo 📦 Añadiendo mcp-access como submodule...
    git submodule add https://github.com/ardelperal/mcp-access.git mcp-modules/mcp-access
) else (
    echo 🔄 Actualizando mcp-access existente...
    cd mcp-modules\mcp-access
    git pull origin main
    cd ..\..
)

REM Inicializar submodules
git submodule update --init --recursive

REM Crear configuración MCP si no existe
if not exist "mcp.json" (
    echo ⚙️ Creando configuración MCP...
    echo {> mcp.json
    echo   "mcpServers": {>> mcp.json
    echo     "mcp-access": {>> mcp.json
    echo       "command": "python",>> mcp.json
    echo       "args": ["mcp-modules/mcp-access/src/mcp_access_server.py"],>> mcp.json
    echo       "env": {>> mcp.json
    echo         "PYTHONPATH": "mcp-modules/mcp-access/src">> mcp.json
    echo       }>> mcp.json
    echo     }>> mcp.json
    echo   }>> mcp.json
    echo }>> mcp.json
)

REM Instalar dependencias
echo 📋 Instalando dependencias...
if exist "mcp-modules\mcp-access\requirements.txt" (
    pip install -r mcp-modules\mcp-access\requirements.txt
)

REM Ejecutar configuración automática
echo 🔧 Ejecutando configuración automática...
cd mcp-modules\mcp-access
python scripts\setup\auto_setup.py
cd ..\..

echo ✅ MCP Access Database configurado correctamente!
echo 📖 Consulta mcp-modules\mcp-access\README.md para más información
pause