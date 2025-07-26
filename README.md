# MCP Access Database Server

Un servidor MCP (Model Context Protocol) profesional para manipular bases de datos de Microsoft Access usando Python, con detección automática de proxy para entornos corporativos.

## 🚀 Características

- ✅ **Conectividad Access**: Soporte completo para .accdb y .mdb
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
├── 📁 src/                    # Código fuente
│   ├── mcp_access_server.py   # Servidor MCP principal
│   └── config.py              # Configuración
├── 📁 scripts/                # Scripts de instalación y utilidades
│   ├── 📁 setup/              # Scripts de configuración
│   │   ├── auto_setup.py      # Configuración automática
│   │   ├── setup_with_proxy_detection.bat
│   │   ├── quick_setup.bat
│   │   ├── install.bat
│   │   └── configure_claude.bat
│   └── 📁 utils/              # Utilidades
│       ├── detect_proxy.py    # Detección de proxy
│       ├── start.bat          # Iniciar servidor
│       ├── sync_mcp.bat       # Sincronización
│       └── sync_mcp.sh
├── 📁 tools/                  # Herramientas de desarrollo
│   ├── test_pip_install.py    # Pruebas de conectividad
│   ├── test_ivanti_detection.py
│   └── test_final_summary.py
├── 📁 tests/                  # Pruebas unitarias
├── 📁 examples/               # Ejemplos de uso
└── 📁 docs/                   # Documentación
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
- `connect_database`: Conectar a una base de datos Access
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

### Conectar y Listar Tablas
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

## 🔧 Solución de Problemas

### Error de Conectividad
1. Verificar configuración de proxy: `python tools/test_pip_install.py`
2. Comprobar Access Database Engine instalado
3. Verificar permisos de archivo de base de datos

### Error de Configuración MCP
1. Ejecutar `install.bat` nuevamente
2. Verificar ruta en configuración de Trae
3. Reiniciar Trae AI

## 📖 Documentación Adicional

- [Documentación Técnica](docs/technical_documentation.md)
- [Guía de Instalación Local](INSTALL_LOCAL.md)
- [Guía de Sincronización](SYNC_GUIDE.md)

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