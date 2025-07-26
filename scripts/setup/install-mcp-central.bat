@echo off
REM install-mcp-central.bat - Instalación centralizada del MCP Access Database

echo 🎯 Instalación Centralizada - MCP Access Database
echo ================================================

REM Definir directorio central
set MCP_DIR=C:\MCPs
set MCP_ACCESS_DIR=%MCP_DIR%\mcp-access

echo 📁 Creando directorio central de MCPs...
if not exist "%MCP_DIR%" mkdir "%MCP_DIR%"

REM Verificar si ya existe
if exist "%MCP_ACCESS_DIR%" (
    echo 🔄 Actualizando MCP Access existente...
    cd "%MCP_ACCESS_DIR%"
    git pull origin main
) else (
    echo 📦 Clonando MCP Access Database...
    cd "%MCP_DIR%"
    git clone https://github.com/ardelperal/mcp-access.git mcp-access
    cd mcp-access
)

REM Instalar dependencias
echo 📋 Instalando dependencias...
pip install -r requirements.txt

REM Configuración automática
echo ⚙️ Ejecutando configuración automática...
python scripts\setup\auto_setup.py

echo ✅ MCP Access Database instalado centralmente en: %MCP_ACCESS_DIR%
echo 📖 Para usar en proyectos, configura la ruta: %MCP_ACCESS_DIR%\src\mcp_access_server.py

pause