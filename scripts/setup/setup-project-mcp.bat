@echo off
REM setup-project-mcp.bat - Configura MCP centralizado en proyecto actual

echo 🔗 Configurando MCP Access Database centralizado...

REM Verificar que existe la instalación central
set MCP_ACCESS_DIR=C:\MCPs\mcp-access
if not exist "%MCP_ACCESS_DIR%" (
    echo ❌ Error: MCP Access no encontrado en %MCP_ACCESS_DIR%
    echo 📦 Ejecuta primero: install-mcp-central.bat
    pause
    exit /b 1
)

REM Crear configuración MCP para este proyecto
echo ⚙️ Creando configuración MCP...
echo {> mcp.json
echo   "mcpServers": {>> mcp.json
echo     "mcp-access": {>> mcp.json
echo       "command": "python",>> mcp.json
echo       "args": ["%MCP_ACCESS_DIR:\=/%/src/mcp_access_server.py"],>> mcp.json
echo       "env": {>> mcp.json
echo         "PYTHONPATH": "%MCP_ACCESS_DIR:\=/%/src">> mcp.json
echo       }>> mcp.json
echo     }>> mcp.json
echo   }>> mcp.json
echo }>> mcp.json

REM Verificar que las dependencias están instaladas
echo 📋 Verificando dependencias...
python -c "import pyodbc" 2>nul
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install -r "%MCP_ACCESS_DIR%\requirements.txt"
)

echo ✅ Proyecto configurado para usar MCP Access centralizado
echo 📁 Configuración creada: mcp.json
echo 🎯 MCP ubicado en: %MCP_ACCESS_DIR%

pause