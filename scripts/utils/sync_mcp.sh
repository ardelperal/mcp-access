#!/bin/bash
# sync_mcp.sh - Script de sincronización para múltiples máquinas

set -e

# Configuración
REPO_URL="https://github.com/TU_USUARIO/mcp-access-database.git"
MCP_DIR="$HOME/.mcp/servers/mcp-access"
CONFIG_FILE="$HOME/.mcp/config.json"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 MCP Access Database - Sincronización${NC}"
echo "=================================================="

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Verificar si Git está instalado
if ! command -v git &> /dev/null; then
    error "Git no está instalado. Por favor instala Git primero."
fi

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    error "Python no está instalado. Por favor instala Python 3.8+ primero."
fi

# Crear directorio base si no existe
mkdir -p "$(dirname "$MCP_DIR")"

# Función para clonar o actualizar el repositorio
sync_repository() {
    if [ -d "$MCP_DIR/.git" ]; then
        log "Actualizando repositorio existente..."
        cd "$MCP_DIR"
        git fetch origin
        git reset --hard origin/main
        log "Repositorio actualizado"
    else
        log "Clonando repositorio..."
        if [ -d "$MCP_DIR" ]; then
            rm -rf "$MCP_DIR"
        fi
        git clone "$REPO_URL" "$MCP_DIR"
        log "Repositorio clonado"
    fi
}

# Función para instalar dependencias
install_dependencies() {
    log "Instalando dependencias..."
    cd "$MCP_DIR"
    
    # Usar pip3 si está disponible, sino pip
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements.txt
    else
        error "pip no está disponible"
    fi
    
    log "Dependencias instaladas"
}

# Función para configurar el MCP
configure_mcp() {
    log "Configurando MCP..."
    
    # Crear configuración si no existe
    if [ ! -f "$CONFIG_FILE" ]; then
        mkdir -p "$(dirname "$CONFIG_FILE")"
        cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {}
}
EOF
    fi
    
    # Actualizar configuración con jq si está disponible
    if command -v jq &> /dev/null; then
        # Crear configuración temporal
        cat > /tmp/mcp_access_config.json << EOF
{
  "access-db": {
    "command": "python3",
    "args": [
      "$MCP_DIR/src/mcp_access_server.py"
    ],
    "env": {
      "PYTHONPATH": "$MCP_DIR/src",
      "MCP_ACCESS_LOG_LEVEL": "INFO"
    },
    "description": "Microsoft Access Database MCP Server"
  }
}
EOF
        
        # Fusionar configuraciones
        jq '.mcpServers += input' "$CONFIG_FILE" /tmp/mcp_access_config.json > /tmp/merged_config.json
        mv /tmp/merged_config.json "$CONFIG_FILE"
        rm /tmp/mcp_access_config.json
        
        log "Configuración actualizada con jq"
    else
        warning "jq no está disponible. Configuración manual requerida."
        echo "Agrega esta configuración a $CONFIG_FILE:"
        cat "$MCP_DIR/trae_config.json"
    fi
}

# Función para verificar la instalación
verify_installation() {
    log "Verificando instalación..."
    
    cd "$MCP_DIR"
    if python3 src/mcp_access_server.py --version 2>/dev/null || python src/mcp_access_server.py --version 2>/dev/null; then
        log "✅ MCP verificado correctamente"
    else
        warning "No se pudo verificar el MCP"
    fi
}

# Función principal
main() {
    log "Iniciando sincronización..."
    
    sync_repository
    install_dependencies
    configure_mcp
    verify_installation
    
    echo ""
    echo -e "${GREEN}🎉 Sincronización completada!${NC}"
    echo "MCP instalado en: $MCP_DIR"
    echo "Configuración en: $CONFIG_FILE"
    echo ""
    echo "Para usar en Trae 2.0, reinicia la aplicación."
}

# Ejecutar función principal
main "$@"