#!/bin/bash
# setup-project-mcp.sh - Configura MCP centralizado en proyecto actual

echo "🔗 Configurando MCP Access Database centralizado..."

# Verificar que existe la instalación central
MCP_ACCESS_DIR="$HOME/MCPs/mcp-access"
if [ ! -d "$MCP_ACCESS_DIR" ]; then
    echo "❌ Error: MCP Access no encontrado en $MCP_ACCESS_DIR"
    echo "📦 Ejecuta primero: install-mcp-central.sh"
    exit 1
fi

# Crear configuración MCP para este proyecto
echo "⚙️ Creando configuración MCP..."
cat > mcp.json << EOF
{
  "mcpServers": {
    "mcp-access": {
      "command": "python",
      "args": ["$MCP_ACCESS_DIR/src/mcp_access_server.py"],
      "env": {
        "PYTHONPATH": "$MCP_ACCESS_DIR/src"
      }
    }
  }
}
EOF

# Verificar que las dependencias están instaladas
echo "📋 Verificando dependencias..."
if ! python -c "import pyodbc" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r "$MCP_ACCESS_DIR/requirements.txt"
fi

echo "✅ Proyecto configurado para usar MCP Access centralizado"
echo "📁 Configuración creada: mcp.json"
echo "🎯 MCP ubicado en: $MCP_ACCESS_DIR"