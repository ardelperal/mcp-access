# 🔗 Guía de Integración - MCP Access Database

Esta guía explica cómo integrar el **MCP Access Database** en otros proyectos.

## 📋 Requisitos Previos

- Git instalado
- Python 3.8+
- Proyecto git inicializado
- Acceso a bases de datos Access (.mdb/.accdb)

## 🚀 Métodos de Integración

### 1. **Instalación Centralizada (Recomendado para Múltiples Proyectos)**

Si planeas usar este MCP en múltiples proyectos, la mejor práctica es instalarlo centralmente:

#### Estructura Centralizada
```
C:/MCPs/                     # Windows
├── mcp-access/
│   ├── src/
│   ├── scripts/
│   └── tools/

~/MCPs/                      # Linux/macOS
├── mcp-access/
│   ├── src/
│   ├── scripts/
│   └── tools/
```

#### Instalación Central - Windows
```batch
# Descargar e instalar centralmente
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/install-mcp-central.bat
install-mcp-central.bat
```

#### Instalación Central - Linux/macOS
```bash
# Descargar e instalar centralmente
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/install-mcp-central.sh
chmod +x install-mcp-central.sh
./install-mcp-central.sh
```

#### Configurar Proyecto Individual
En cada proyecto que use el MCP:

**Windows:**
```batch
# Descargar script de configuración
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/setup-project-mcp.bat
setup-project-mcp.bat
```

**Linux/macOS:**
```bash
# Descargar script de configuración
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/setup-project-mcp.sh
chmod +x setup-project-mcp.sh
./setup-project-mcp.sh
```

#### Ventajas de la Instalación Centralizada
- ✅ Una sola instalación para todos los proyectos
- ✅ Actualizaciones centralizadas
- ✅ Menor uso de espacio en disco
- ✅ Configuración consistente
- ✅ Fácil mantenimiento

### 2. **Git Submodule (Para Desarrollo)**

#### Paso 1: Añadir como Submodule
```bash
# En el directorio raíz de tu proyecto
git submodule add https://github.com/ardelperal/mcp-access.git mcp-modules/mcp-access
git submodule update --init --recursive
```

#### Paso 2: Configurar MCP
Crea o actualiza tu archivo `mcp.json`:
```json
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
```

#### Paso 3: Instalar Dependencias
```bash
pip install -r mcp-modules/mcp-access/requirements.txt
```

#### Paso 4: Configuración Automática
```bash
cd mcp-modules/mcp-access
python scripts/setup/auto_setup.py
```

### 3. **Instalación Automática por Proyecto**

#### Para Linux/macOS:
```bash
# Descargar y ejecutar script
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/setup-mcp-access.sh
chmod +x setup-mcp-access.sh
./setup-mcp-access.sh
```

#### Para Windows:
```batch
REM Descargar y ejecutar script
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/setup-mcp-access.bat
setup-mcp-access.bat
```

### 4. **Fork y Personalización**

Si necesitas modificaciones específicas:

```bash
# Fork del repositorio en GitHub
# Luego clona tu fork
git submodule add https://github.com/TU_USUARIO/mcp-access.git mcp-modules/mcp-access
```

## ⚙️ Configuración Avanzada

### Variables de Entorno
```bash
# Configurar proxy si es necesario
export HTTP_PROXY=http://proxy.empresa.com:8080
export HTTPS_PROXY=http://proxy.empresa.com:8080

# Configurar ruta de base de datos por defecto
export MCP_ACCESS_DEFAULT_DB="C:/ruta/a/tu/base.accdb"
```

### Configuración de Trae AI
```json
{
  "mcpServers": {
    "mcp-access": {
      "command": "python",
      "args": ["mcp-modules/mcp-access/src/mcp_access_server.py"],
      "env": {
        "PYTHONPATH": "mcp-modules/mcp-access/src",
        "MCP_ACCESS_DEFAULT_DB": "C:/ruta/a/tu/base.accdb"
      }
    }
  }
}
```

## 🔄 Actualización del MCP

### Actualizar Submodule
```bash
cd mcp-modules/mcp-access
git pull origin main
cd ../..
git add mcp-modules/mcp-access
git commit -m "Update mcp-access submodule"
```

### Actualización Automática
```bash
# Script para actualizar automáticamente
git submodule update --remote mcp-modules/mcp-access
```

## 🧪 Verificación de la Instalación

### Test Básico
```python
# test_mcp_integration.py
import subprocess
import json

def test_mcp_access():
    """Verifica que el MCP Access esté funcionando"""
    try:
        # Ejecutar el servidor MCP
        result = subprocess.run([
            "python", 
            "mcp-modules/mcp-access/src/mcp_access_server.py"
        ], capture_output=True, text=True, timeout=10)
        
        print("✅ MCP Access Database integrado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en la integración: {e}")
        return False

if __name__ == "__main__":
    test_mcp_access()
```

### Diagnóstico Completo
```bash
# Ejecutar herramientas de diagnóstico
python mcp-modules/mcp-access/tools/test_final_summary.py
```

## 📁 Estructura del Proyecto Integrado

```
tu-proyecto/
├── mcp-modules/
│   └── mcp-access/          # Submodule del MCP
│       ├── src/
│       ├── scripts/
│       ├── tools/
│       └── docs/
├── mcp.json                 # Configuración MCP
├── requirements.txt         # Dependencias del proyecto
└── tu-codigo/
```

## 🔧 Personalización

### Configuración Específica del Proyecto
```python
# config/mcp_config.py
MCP_ACCESS_CONFIG = {
    "default_database": "data/proyecto.accdb",
    "connection_timeout": 30,
    "enable_logging": True,
    "log_level": "INFO"
}
```

### Wrapper Personalizado
```python
# utils/mcp_wrapper.py
from mcp_modules.mcp_access.src import mcp_access_server

class ProjectMCPAccess:
    def __init__(self, db_path=None):
        self.db_path = db_path or "data/default.accdb"
        
    def query_data(self, table, filters=None):
        """Wrapper personalizado para consultas"""
        # Tu lógica específica aquí
        pass
```

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error de Proxy**
   ```bash
   cd mcp-modules/mcp-access
   python scripts/utils/detect_proxy.py
   ```

2. **Error de Base de Datos**
   ```bash
   python mcp-modules/mcp-access/tools/test_ivanti_detection.py
   ```

3. **Error de Dependencias**
   ```bash
   pip install -r mcp-modules/mcp-access/requirements.txt --force-reinstall
   ```

## 📞 Soporte

- **Documentación**: `mcp-modules/mcp-access/docs/`
- **Issues**: https://github.com/ardelperal/mcp-access/issues
- **Wiki**: https://github.com/ardelperal/mcp-access/wiki

## 🔄 Contribuir

Si realizas mejoras, considera contribuir al proyecto principal:

```bash
cd mcp-modules/mcp-access
git checkout -b feature/mi-mejora
# Realizar cambios
git commit -m "Add: mi mejora"
git push origin feature/mi-mejora
# Crear Pull Request en GitHub
```

---

**¡Listo!** Tu proyecto ahora tiene acceso completo a bases de datos Access a través del MCP.