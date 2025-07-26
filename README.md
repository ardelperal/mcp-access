# MCP Access Database Server

Un servidor MCP (Model Context Protocol) para manipular bases de datos de Microsoft Access usando Python.

## Características

- ✅ Conectar a bases de datos Access (.accdb y .mdb)
- ✅ Crear, leer, actualizar y eliminar tablas
- ✅ Ejecutar consultas SQL personalizadas
- ✅ Listar todas las tablas y sus campos
- ✅ Insertar, actualizar y eliminar registros
- ✅ Obtener esquema de la base de datos

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Asegúrate de tener el Microsoft Access Database Engine instalado:
   - Para sistemas de 64 bits: Microsoft Access Database Engine 2016 Redistributable
   - Para sistemas de 32 bits: Microsoft Access Database Engine 2010 Redistributable

## Uso

El servidor MCP se ejecuta automáticamente cuando se configura en un cliente MCP compatible.

### Herramientas disponibles:

- `connect_database`: Conectar a una base de datos Access
- `list_tables`: Listar todas las tablas
- `get_table_schema`: Obtener esquema de una tabla
- `create_table`: Crear nueva tabla
- `drop_table`: Eliminar tabla
- `execute_query`: Ejecutar consulta SQL
- `insert_record`: Insertar registro
- `update_record`: Actualizar registro
- `delete_record`: Eliminar registro
- `get_records`: Obtener registros de una tabla

## Configuración

Configura el servidor en tu cliente MCP añadiendo esta configuración:

```json
{
  "mcpServers": {
    "access-db": {
      "command": "python",
      "args": ["src/mcp_access_server.py"],
      "env": {}
    }
  }
}
```