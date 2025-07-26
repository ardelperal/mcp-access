#!/bin/bash
# install-mcp-central.sh - Instalación centralizada del MCP Access Database

echo "🎯 Instalación Centralizada - MCP Access Database"
echo "================================================"

# Definir directorio central
MCP_DIR="$HOME/MCPs"
MCP_ACCESS_DIR="$MCP_DIR/mcp-access"

echo "📁 Creando directorio central de MCPs..."
mkdir -p "$MCP_DIR"

# Verificar si ya existe
if [ -d "$MCP_ACCESS_DIR" ]; then
    echo "🔄 Actualizando MCP Access existente..."
    cd "$MCP_ACCESS_DIR"
    git pull origin main
else
    echo "📦 Clonando MCP Access Database..."
    cd "$MCP_DIR"
    git clone https://github.com/ardelperal/mcp-access.git mcp-access
    cd mcp-access
fi

# Instalar dependencias
echo "📋 Instalando dependencias..."
pip install -r requirements.txt

# Configuración automática
echo "⚙️ Ejecutando configuración automática..."
python scripts/setup/auto_setup.py

echo "✅ MCP Access Database instalado centralmente en: $MCP_ACCESS_DIR"
echo "📖 Para usar en proyectos, configura la ruta: $MCP_ACCESS_DIR/src/mcp_access_server.py"