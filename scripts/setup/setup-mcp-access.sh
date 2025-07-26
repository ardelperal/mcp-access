#!/bin/bash
# setup-mcp-access.sh - Script para integrar mcp-access en otro proyecto

echo "🚀 Configurando MCP Access Database..."

# Verificar si es un repositorio git
if [ ! -d ".git" ]; then
    echo "❌ Error: Este directorio no es un repositorio git"
    exit 1
fi

# Crear directorio para módulos MCP si no existe
mkdir -p mcp-modules

# Añadir como submodule si no existe
if [ ! -d "mcp-modules/mcp-access" ]; then
    echo "📦 Añadiendo mcp-access como submodule..."
    git submodule add https://github.com/ardelperal/mcp-access.git mcp-modules/mcp-access
else
    echo "🔄 Actualizando mcp-access existente..."
    cd mcp-modules/mcp-access
    git pull origin main
    cd ../..
fi

# Inicializar submodules
git submodule update --init --recursive

# Crear configuración MCP si no existe
if [ ! -f "mcp.json" ]; then
    echo "⚙️ Creando configuración MCP..."
    cat > mcp.json << 'EOF'
{
  "mcpServers": {
    "mcp-access": {
      "command": "python",
      "args": ["mcp-modules/mcp-access/src/mcp_access_server.py"],
      "env": {
        "PYTHONPATH": "mcp-modules/mcp-access/src"
      }
    }
  }
}
EOF
fi

# Instalar dependencias
echo "📋 Instalando dependencias..."
if [ -f "mcp-modules/mcp-access/requirements.txt" ]; then
    pip install -r mcp-modules/mcp-access/requirements.txt
fi

# Ejecutar configuración automática
echo "🔧 Ejecutando configuración automática..."
cd mcp-modules/mcp-access
python scripts/setup/auto_setup.py
cd ../..

echo "✅ MCP Access Database configurado correctamente!"
echo "📖 Consulta mcp-modules/mcp-access/README.md para más información"