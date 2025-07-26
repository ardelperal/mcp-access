# Documentación Técnica - MCP Access Database

## Arquitectura del Sistema

### Componentes Principales

1. **Servidor MCP** (`src/mcp_access_server.py`)
   - Implementa el protocolo Model Context Protocol
   - Maneja conexiones a bases de datos Access
   - Expone herramientas para operaciones CRUD

2. **Detector de Proxy** (`scripts/utils/detect_proxy.py`)
   - Detecta configuraciones de proxy automáticamente
   - Soporte específico para Ivanti VPN
   - Configura pip y git automáticamente

3. **Sistema de Instalación** (`scripts/setup/`)
   - Instalación automatizada con detección de proxy
   - Configuración de Trae AI
   - Scripts de diagnóstico

## Protocolo MCP

### Herramientas Implementadas

#### `connect_database`
```json
{
  "name": "connect_database",
  "description": "Conectar a una base de datos Access",
  "inputSchema": {
    "type": "object",
    "properties": {
      "database_path": {
        "type": "string",
        "description": "Ruta al archivo .accdb o .mdb"
      }
    },
    "required": ["database_path"]
  }
}
```

#### `execute_query`
```json
{
  "name": "execute_query",
  "description": "Ejecutar consulta SQL",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Consulta SQL a ejecutar"
      },
      "parameters": {
        "type": "array",
        "description": "Parámetros para la consulta"
      }
    },
    "required": ["query"]
  }
}
```

## Detección de Proxy

### Métodos de Detección

1. **WinHTTP Settings**
   ```python
   def get_winhttp_proxy():
       # Lee configuración de WinHTTP del registro
       # HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\Connections
   ```

2. **Internet Explorer Settings**
   ```python
   def get_ie_proxy():
       # Lee configuración de IE del registro
       # HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings
   ```

3. **Variables de Entorno**
   ```python
   def get_env_proxy():
       # Verifica HTTP_PROXY, HTTPS_PROXY, etc.
   ```

4. **Detección Ivanti**
   ```python
   def check_ivanti_connection():
       # Verifica procesos, servicios y adaptadores de red
       # Detecta rutas corporativas específicas
   ```

### Configuración Automática

Cuando se detecta un proxy, el sistema configura automáticamente:

- **pip**: `pip config set global.proxy <proxy_url>`
- **git**: `git config --global http.proxy <proxy_url>`
- **Variables de entorno**: `HTTP_PROXY`, `HTTPS_PROXY`

## Base de Datos Access

### Conexión

El sistema utiliza `pyodbc` con el driver de Microsoft Access:

```python
connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    f'DBQ={database_path};'
)
conn = pyodbc.connect(connection_string)
```

### Operaciones Soportadas

1. **DDL (Data Definition Language)**
   - CREATE TABLE
   - DROP TABLE
   - ALTER TABLE (limitado)

2. **DML (Data Manipulation Language)**
   - SELECT
   - INSERT
   - UPDATE
   - DELETE

3. **Consultas de Metadatos**
   - Listar tablas
   - Obtener esquemas
   - Información de columnas

## Manejo de Errores

### Tipos de Error

1. **Errores de Conexión**
   ```python
   class DatabaseConnectionError(Exception):
       pass
   ```

2. **Errores de SQL**
   ```python
   class SQLExecutionError(Exception):
       pass
   ```

3. **Errores de Proxy**
   ```python
   class ProxyDetectionError(Exception):
       pass
   ```

### Logging

El sistema utiliza logging estructurado:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Configuración de Trae AI

### Archivo de Configuración

La configuración se almacena en `~/.mcp/config.json`:

```json
{
  "mcpServers": {
    "mcp-access": {
      "command": "python",
      "args": ["C:/ruta/completa/src/mcp_access_server.py"],
      "env": {
        "PYTHONPATH": "C:/ruta/completa"
      }
    }
  }
}
```

### Variables de Entorno

- `MCP_ACCESS_DEBUG`: Habilita logging detallado
- `MCP_ACCESS_TIMEOUT`: Timeout para conexiones (segundos)
- `MCP_ACCESS_MAX_ROWS`: Máximo número de filas a retornar

## Seguridad

### Consideraciones

1. **Validación de Entrada**
   - Sanitización de consultas SQL
   - Validación de rutas de archivo
   - Escape de caracteres especiales

2. **Permisos de Archivo**
   - Verificación de permisos de lectura/escritura
   - Validación de rutas permitidas

3. **Inyección SQL**
   - Uso de parámetros preparados
   - Validación de sintaxis SQL

## Rendimiento

### Optimizaciones

1. **Pool de Conexiones**
   ```python
   class ConnectionPool:
       def __init__(self, max_connections=5):
           self.max_connections = max_connections
           self.connections = []
   ```

2. **Cache de Metadatos**
   ```python
   @lru_cache(maxsize=100)
   def get_table_schema(table_name):
       # Cache de esquemas de tabla
   ```

3. **Paginación**
   ```python
   def get_records(table, limit=1000, offset=0):
       # Implementa paginación para grandes datasets
   ```

## Testing

### Estructura de Tests

```
tools/
├── test_pip_install.py      # Test de conectividad pip
├── test_ivanti_detection.py # Test de detección Ivanti
└── test_final_summary.py    # Test completo del sistema
```

### Ejecución de Tests

```bash
# Test individual
python tools/test_pip_install.py

# Test completo
python tools/test_final_summary.py
```

## Troubleshooting

### Problemas Comunes

1. **Error: "Driver not found"**
   - Instalar Microsoft Access Database Engine
   - Verificar arquitectura (32-bit vs 64-bit)

2. **Error: "Access denied"**
   - Verificar permisos de archivo
   - Ejecutar como administrador si es necesario

3. **Error: "Proxy connection failed"**
   - Verificar configuración de proxy
   - Ejecutar `python scripts/utils/detect_proxy.py`

### Logs de Diagnóstico

```bash
# Habilitar logging detallado
set MCP_ACCESS_DEBUG=1
python src/mcp_access_server.py
```

## Desarrollo

### Estructura del Código

```python
# Patrón de diseño utilizado
class MCPAccessServer:
    def __init__(self):
        self.tools = self._register_tools()
    
    def _register_tools(self):
        return [
            Tool("connect_database", self.connect_database),
            Tool("execute_query", self.execute_query),
            # ...
        ]
```

### Extensibilidad

Para añadir nuevas herramientas:

1. Definir la función handler
2. Registrar en `_register_tools()`
3. Añadir documentación
4. Crear tests

### Contribución

1. Fork del repositorio
2. Crear rama feature
3. Implementar cambios
4. Añadir tests
5. Crear Pull Request