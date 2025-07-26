# MCP Access Database Server

Un servidor MCP (Model Context Protocol) profesional para manipular bases de datos de Microsoft Access usando Python, con detección automática de proxy para entornos corporativos.

## 🚀 Características

- ✅ **Conectividad Access**: Soporte completo para .accdb y .mdb
- ✅ **Bases de Datos Protegidas**: Soporte para bases de datos con contraseña
- ✅ **Operaciones CRUD**: Crear, leer, actualizar y eliminar tablas y registros
- ✅ **Consultas SQL**: Ejecutar consultas SQL personalizadas
- ✅ **Esquemas**: Listar tablas, campos y obtener estructura completa
- ✅ **Detección de Proxy**: Configuración automática para entornos corporativos
- ✅ **Detección Ivanti**: Soporte específico para VPN Ivanti
- ✅ **Instalación Guiada**: Scripts de configuración automática

## 📁 Estructura del Proyecto

```
mcp-access/
├── 📄 install.bat              # Instalador principal
├── 📄 requirements.txt         # Dependencias Python
├── 📄 mcp.json                # Configuración MCP
├── 📄 setup.py                # Configuración de instalación
├── 📁 src/                    # Código fuente
│   ├── mcp_access_server.py   # Servidor MCP principal
│   ├── enhanced_documentation.py # Generación de documentación
│   └── config.py              # Configuración
├── 📁 scripts/                # Scripts de instalación y utilidades
│   ├── 📁 setup/              # Scripts de configuración
│   └── 📁 utils/              # Utilidades (detección proxy, etc.)
├── 📁 tests/                  # Pruebas y ejemplos
│   ├── demo_complete_functionality.py
│   ├── test_mcp_access.py     # Pruebas principales
│   ├── test_com_relationships.py
│   └── 📁 sample_databases/   # Bases de datos de ejemplo
├── 📁 tools/                  # Herramientas de desarrollo
│   ├── test_integration.py    # Pruebas de integración
│   └── test_pip_install.py    # Pruebas de conectividad
├── 📁 examples/               # Ejemplos de uso
│   ├── mcp-integration-example.json
│   └── test_mcp.py
└── 📁 docs/                   # Documentación completa
    ├── technical_documentation.md
    ├── ejemplos_prompts.md    # Ejemplos de uso
    ├── implementation_summary.md
    └── relationship_detection.md
```

## ⚡ Instalación Rápida

### Opción 1: Instalador Automático (Recomendado)
```bash
# Ejecutar el instalador principal
install.bat
```

### Opción 2: Instalación Manual
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar automáticamente
python scripts/setup/auto_setup.py
```

## 🔧 Requisitos del Sistema

- **Python 3.8+**
- **Microsoft Access Database Engine**:
  - 64-bit: [Access Database Engine 2016 Redistributable](https://www.microsoft.com/download/details.aspx?id=54920)
  - 32-bit: [Access Database Engine 2010 Redistributable](https://www.microsoft.com/download/details.aspx?id=13255)

## 🛠️ Herramientas Disponibles

### Conexión y Gestión
- `connect_database`: Conectar a una base de datos Access (con soporte para contraseñas)
- `list_tables`: Listar todas las tablas disponibles
- `get_table_schema`: Obtener esquema detallado de una tabla

### Operaciones de Tabla
- `create_table`: Crear nueva tabla con campos especificados
- `drop_table`: Eliminar tabla existente

### Operaciones de Datos
- `execute_query`: Ejecutar consultas SQL personalizadas
- `insert_record`: Insertar nuevo registro
- `update_record`: Actualizar registro existente
- `delete_record`: Eliminar registro
- `get_records`: Obtener registros con filtros opcionales

### Análisis de Estructura y Relaciones 🆕
- `get_table_relationships`: Obtener todas las relaciones entre tablas (claves foráneas)
- `get_table_indexes`: Obtener los índices de una tabla específica
- `get_primary_keys`: Obtener las claves primarias de una tabla

### Documentación Automática 🆕
- `generate_database_documentation`: Generar documentación completa de la base de datos
- `export_documentation_markdown`: Exportar documentación en formato Markdown

#### Características de la Documentación Automática
- **Análisis completo de estructura**: Esquemas de tablas, tipos de datos, restricciones
- **Detección de relaciones**: Identificación automática de claves foráneas y relaciones entre tablas
- **Índices y claves primarias**: Documentación detallada de todos los índices
- **Conteo de registros**: Estadísticas de cada tabla
- **Formato Markdown**: Exportación en formato legible y profesional
- **Manejo robusto de errores**: Funciona incluso con bases de datos con problemas de codificación o permisos
- **Compatibilidad extendida**: Soporte para diferentes versiones de Access y configuraciones ODBC

## ⚙️ Configuración para Trae AI

### Configuración Automática
El instalador configura automáticamente Trae AI. La configuración se añade a `~/.mcp/config.json`:

```json
{
  "mcpServers": {
    "mcp-access": {
      "command": "python",
      "args": ["C:/ruta/al/proyecto/src/mcp_access_server.py"],
      "env": {}
    }
  }
}
```

### Configuración Manual
Si necesitas configurar manualmente:

1. Abrir Trae AI
2. Ir a Configuración → MCP Servers
3. Añadir nuevo servidor con la configuración anterior

## 🌐 Soporte para Entornos Corporativos

### Detección Automática de Proxy
- ✅ Detección de configuración WinHTTP
- ✅ Detección de configuración Internet Explorer/Edge
- ✅ Soporte para variables de entorno
- ✅ Detección específica de Ivanti VPN

### Configuración Manual de Proxy
```bash
# Configurar proxy para pip
python scripts/utils/detect_proxy.py

# O configurar manualmente
pip config set global.proxy http://proxy.empresa.com:8080
```

## 🧪 Herramientas de Diagnóstico

```bash
# Probar conectividad pip
python tools/test_pip_install.py

# Verificar detección de Ivanti
python tools/test_ivanti_detection.py

# Resumen completo de configuración
python tools/test_final_summary.py
```

## 📚 Ejemplos de Uso

### Conectar a Base de Datos
```python
# Conectar sin contraseña
connect_database(database_path="C:/ruta/mi_base.accdb")

# Conectar con contraseña específica
connect_database(database_path="C:/ruta/mi_base.accdb", password="mi_contraseña")

# Conectar usando contraseña por defecto (dpddpd)
connect_database(database_path="C:/ruta/mi_base.accdb", password="dpddpd")

# Si no se especifica contraseña, se intenta primero con "dpddpd" y luego sin contraseña
connect_database(database_path="C:/ruta/mi_base.accdb")
```

### Consultas y Operaciones
```python
# El servidor MCP maneja automáticamente las conexiones
# Usar desde Trae AI o cliente MCP compatible

# Ejemplo de consulta
SELECT * FROM Empleados WHERE Departamento = 'IT'
```

### Crear Nueva Tabla
```python
# Definir estructura de tabla
campos = [
    {"nombre": "ID", "tipo": "AUTOINCREMENT"},
    {"nombre": "Nombre", "tipo": "TEXT(50)"},
    {"nombre": "Email", "tipo": "TEXT(100)"}
]
```


### Análisis y Documentación de Base de Datos 🆕

```python
# Ejemplo completo de análisis de base de datos
from mcp_access_server import AccessDatabaseManager

# Conectar a la base de datos
db_manager = AccessDatabaseManager()
db_manager.connect("C:/mi_proyecto/datos.accdb", password="mi_contraseña")

# Obtener información de estructura
tables = db_manager.list_tables()
print(f"Tablas encontradas: {len(tables)}")

# Analizar una tabla específica
table_name = "empleados"
schema = db_manager.get_table_schema(table_name)
primary_keys = db_manager.get_primary_keys(table_name)
indexes = db_manager.get_table_indexes(table_name)

print(f"Esquema de {table_name}:")
for column in schema:
    print(f"  - {column['column_name']}: {column['data_type']}")

# Generar documentación completa
documentation = db_manager.generate_database_documentation()
print(f"Documentación generada para {documentation['summary']['total_tables']} tablas")

# Exportar a Markdown
markdown_content = db_manager.export_documentation_markdown()
with open("documentacion_bd.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

# Desconectar
db_manager.disconnect()
```

### Ejemplo de Script de Prueba

```python
# Script de prueba completo (similar a test_lanzadera_datos.py)
import os
from src.mcp_access_server import AccessDatabaseManager

def test_database_analysis():
    # Configurar rutas
    db_path = "tests/sample_databases/mi_base.accdb"
    output_path = "tests/sample_databases/documentacion.md"
    
    # Crear manager y conectar
    db_manager = AccessDatabaseManager()
    
    try:
        print("🔌 Conectando a la base de datos...")
        db_manager.connect(db_path)
        
        print("📋 Listando tablas...")
        tables = db_manager.list_tables()
        print(f"   Encontradas {len(tables)} tablas")
        
        print("🔍 Analizando esquemas...")
        for table in tables[:3]:  # Primeras 3 tablas
            schema = db_manager.get_table_schema(table)
            print(f"   {table}: {len(schema)} columnas")
        
        print("🔗 Analizando relaciones...")
        relationships = db_manager.get_table_relationships()
        print(f"   Encontradas {len(relationships)} relaciones")
        
        print("📊 Generando documentación...")
        documentation = db_manager.generate_database_documentation()
        
        print("📝 Exportando a Markdown...")
        markdown_content = db_manager.export_documentation_markdown()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Documentación guardada en: {output_path}")
        
        # Estadísticas finales
        total_records = sum(table.get('record_count', 0) 
                          for table in documentation['tables'].values())
        print(f"📈 Resumen:")
        print(f"   - Tablas: {documentation['summary']['total_tables']}")
        print(f"   - Relaciones: {documentation['summary']['total_relationships']}")
        print(f"   - Registros totales: {total_records}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if db_manager.is_connected():
            db_manager.disconnect()
            print("🔌 Desconectado de la base de datos")

if __name__ == "__main__":
    test_database_analysis()
```

### Ejemplos de Uso de Nuevas Funcionalidades

```json
// Conectar a base de datos con contraseña
{
  "tool": "connect_database",
  "arguments": {
    "database_path": "C:\\mi_proyecto\\datos.accdb",
    "password": "mi_contraseña"
  }
}

// Obtener relaciones entre tablas
{
  "tool": "get_table_relationships",
  "arguments": {}
}

// Obtener índices de una tabla
{
  "tool": "get_table_indexes",
  "arguments": {
    "table_name": "empleados"
  }
}

// Generar documentación completa
{
  "tool": "generate_database_documentation",
  "arguments": {}
}

// Exportar documentación en Markdown
{
  "tool": "export_documentation_markdown",
  "arguments": {}
}

// Crear tabla con relaciones
{
  "tool": "create_table",
  "arguments": {
    "table_name": "pedidos",
    "columns": [
      {"name": "id", "type": "INTEGER", "primary_key": true},
      {"name": "cliente_id", "type": "INTEGER", "not_null": true},
      {"name": "fecha", "type": "DATE"},
      {"name": "total", "type": "DOUBLE"}
    ]
  }
}
```

## 🔧 Solución de Problemas

### Error de Conectividad
1. Verificar configuración de proxy: `python tools/test_pip_install.py`
2. Comprobar Access Database Engine instalado
3. Verificar permisos de archivo de base de datos
4. **Verificar contraseña de la base de datos**:
   - Si la base de datos tiene contraseña, especificarla en el parámetro `password`
   - Por defecto se intenta con "dpddpd" si no se especifica contraseña
   - Si falla con contraseña, se intenta sin contraseña automáticamente

### Error de Configuración MCP
1. Ejecutar `install.bat` nuevamente
2. Verificar ruta en configuración de Trae
3. Reiniciar Trae AI

## 🔗 Integración en Otros Proyectos

### Git Submodule (Para Desarrollo)
```bash
# En tu proyecto, añadir como submodule
git submodule add https://github.com/ardelperal/mcp-access.git mcp-modules/mcp-access
git submodule update --init --recursive

# Instalar dependencias
pip install -r mcp-modules/mcp-access/requirements.txt

# Configurar automáticamente
cd mcp-modules/mcp-access
python scripts/setup/auto_setup.py
```

### Instalación Automática por Proyecto
```bash
# Para Windows
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/setup-mcp-access.bat
setup-mcp-access.bat

# Para Linux/macOS
curl -O https://raw.githubusercontent.com/ardelperal/mcp-access/main/scripts/setup/setup-mcp-access.sh
chmod +x setup-mcp-access.sh
./setup-mcp-access.sh
```

### Verificar Integración
```bash
# Test de integración completo
python tools/test_integration.py
```

## 📖 Documentación Adicional

- [Guía de Integración Completa](INTEGRATION_GUIDE.md)
- [Documentación Técnica](docs/technical_documentation.md)
- [Guía de Instalación Local](INSTALL_LOCAL.md)

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico:
1. Revisar documentación en `docs/`
2. Ejecutar herramientas de diagnóstico en `tools/`
3. Crear issue en GitHub con detalles del problema