# Documentación Técnica - MCP Access Server

## Arquitectura del Sistema

### Componentes Principales

1. **mcp_access_server.py**: Servidor principal MCP
2. **config.py**: Configuración y utilidades
3. **AccessDatabaseManager**: Clase principal para gestión de BD
4. **Herramientas MCP**: 11 herramientas especializadas

### Flujo de Operación

```
Cliente MCP → Servidor MCP → AccessDatabaseManager → pyodbc → Access DB
```

## Herramientas Disponibles

### 1. connect_database
**Propósito**: Establecer conexión con base de datos Access
**Parámetros**:
- `database_path` (string): Ruta completa al archivo .mdb/.accdb

**Ejemplo**:
```json
{
  "database_path": "C:\\datos\\empresa.accdb"
}
```

### 2. disconnect_database
**Propósito**: Cerrar conexión activa
**Parámetros**: Ninguno

### 3. list_tables
**Propósito**: Listar todas las tablas de la BD
**Parámetros**: Ninguno
**Retorna**: Lista de nombres de tablas

### 4. get_table_schema
**Propósito**: Obtener estructura de una tabla
**Parámetros**:
- `table_name` (string): Nombre de la tabla

**Retorna**:
```json
[
  {
    "column_name": "id",
    "data_type": "INTEGER",
    "size": 4,
    "nullable": false,
    "default_value": null
  }
]
```

### 5. create_table
**Propósito**: Crear nueva tabla
**Parámetros**:
- `table_name` (string): Nombre de la tabla
- `columns` (array): Definiciones de columnas

**Ejemplo**:
```json
{
  "table_name": "productos",
  "columns": [
    {
      "name": "id",
      "type": "INTEGER",
      "primary_key": true,
      "not_null": true
    },
    {
      "name": "nombre",
      "type": "TEXT",
      "not_null": true
    },
    {
      "name": "precio",
      "type": "DOUBLE",
      "default": "0"
    }
  ]
}
```

### 6. drop_table
**Propósito**: Eliminar tabla
**Parámetros**:
- `table_name` (string): Nombre de la tabla a eliminar

### 7. execute_query
**Propósito**: Ejecutar consulta SQL personalizada
**Parámetros**:
- `query` (string): Consulta SQL
- `parameters` (array, opcional): Parámetros para la consulta

**Ejemplos**:
```json
{
  "query": "SELECT * FROM empleados WHERE salario > ?",
  "parameters": ["50000"]
}
```

### 8. insert_record
**Propósito**: Insertar nuevo registro
**Parámetros**:
- `table_name` (string): Nombre de la tabla
- `data` (object): Datos a insertar (clave-valor)

**Ejemplo**:
```json
{
  "table_name": "empleados",
  "data": {
    "nombre": "Juan",
    "apellido": "Pérez",
    "salario": 50000
  }
}
```

### 9. update_record
**Propósito**: Actualizar registros existentes
**Parámetros**:
- `table_name` (string): Nombre de la tabla
- `data` (object): Datos a actualizar
- `where_clause` (string): Condición WHERE

**Ejemplo**:
```json
{
  "table_name": "empleados",
  "data": {"salario": 55000},
  "where_clause": "id = 1"
}
```

### 10. delete_record
**Propósito**: Eliminar registros
**Parámetros**:
- `table_name` (string): Nombre de la tabla
- `where_clause` (string): Condición WHERE

### 11. get_records
**Propósito**: Consultar registros con filtros
**Parámetros**:
- `table_name` (string): Nombre de la tabla
- `columns` (array, opcional): Columnas a seleccionar
- `where_clause` (string, opcional): Filtro WHERE
- `order_by` (string, opcional): Orden
- `limit` (integer, opcional): Límite de registros

## Tipos de Datos Soportados

| Tipo Access | Descripción | Ejemplo |
|-------------|-------------|---------|
| TEXT | Texto corto (255 chars) | "Juan Pérez" |
| MEMO | Texto largo (65K chars) | Descripción larga |
| INTEGER | Número entero | 42 |
| LONG | Entero largo | 1000000 |
| DOUBLE | Decimal doble precisión | 3.14159 |
| CURRENCY | Moneda | 1234.56 |
| DATETIME | Fecha y hora | "2023-12-25 15:30:00" |
| YESNO | Booleano | True/False |

## Configuración Avanzada

### Variables de Entorno
- `ACCESS_MCP_LOG_LEVEL`: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
- `ACCESS_MCP_MAX_RECORDS`: Máximo de registros a mostrar (default: 50)

### Configuración de Seguridad
```python
{
  "security": {
    "allow_drop_table": True,
    "allow_delete_records": True,
    "require_where_clause_for_updates": True
  }
}
```

## Manejo de Errores

### Errores Comunes

1. **Driver no encontrado**
   - Error: `[Microsoft][ODBC Driver Manager] Data source name not found`
   - Solución: Instalar Microsoft Access Database Engine

2. **Archivo no encontrado**
   - Error: `Could not find file 'C:\path\to\database.accdb'`
   - Solución: Verificar ruta y permisos

3. **Tabla no existe**
   - Error: `[Microsoft][ODBC Microsoft Access Driver] The Microsoft Jet database engine cannot find the input table or query`
   - Solución: Verificar nombre de tabla

4. **Sintaxis SQL incorrecta**
   - Error: `Syntax error in SQL statement`
   - Solución: Revisar sintaxis SQL específica de Access

### Códigos de Error Personalizados

- `MCP_ACCESS_001`: Error de conexión
- `MCP_ACCESS_002`: Tabla no encontrada
- `MCP_ACCESS_003`: Columna no encontrada
- `MCP_ACCESS_004`: Violación de restricción
- `MCP_ACCESS_005`: Permisos insuficientes

## Optimización y Rendimiento

### Mejores Prácticas

1. **Conexiones**:
   - Reutilizar conexiones cuando sea posible
   - Cerrar conexiones explícitamente
   - Usar pool de conexiones para aplicaciones concurrentes

2. **Consultas**:
   - Usar índices en columnas de búsqueda frecuente
   - Limitar resultados con TOP/LIMIT
   - Evitar SELECT * en tablas grandes

3. **Transacciones**:
   - Agrupar operaciones relacionadas
   - Usar transacciones explícitas para operaciones críticas

### Límites del Sistema

- **Tamaño máximo de BD**: 2 GB (Access 2007+)
- **Registros por tabla**: ~1 millón (práctico)
- **Columnas por tabla**: 255
- **Índices por tabla**: 32
- **Conexiones concurrentes**: Limitadas (recomendado < 10)

## Integración con Clientes MCP

### Claude Desktop
```json
{
  "mcpServers": {
    "access-db": {
      "command": "python",
      "args": ["C:\\ruta\\al\\proyecto\\src\\mcp_access_server.py"],
      "env": {
        "ACCESS_MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Otros Clientes
El servidor es compatible con cualquier cliente que implemente el protocolo MCP estándar.

## Extensiones Futuras

### Funcionalidades Planeadas

1. **Soporte para consultas complejas**:
   - JOINs entre múltiples tablas
   - Subconsultas
   - Funciones agregadas avanzadas

2. **Gestión de índices**:
   - Crear/eliminar índices
   - Análisis de rendimiento

3. **Backup y restauración**:
   - Exportar datos a diferentes formatos
   - Importar desde CSV/Excel

4. **Seguridad avanzada**:
   - Autenticación de usuarios
   - Permisos granulares por tabla

5. **Monitoreo**:
   - Métricas de rendimiento
   - Logs de auditoría

## Solución de Problemas

### Diagnóstico Paso a Paso

1. **Verificar instalación de Python**:
   ```bash
   python --version
   ```

2. **Verificar dependencias**:
   ```bash
   pip list | findstr pyodbc
   pip list | findstr mcp
   ```

3. **Verificar drivers ODBC**:
   ```bash
   python -c "import pyodbc; print(pyodbc.drivers())"
   ```

4. **Probar conexión básica**:
   ```python
   import pyodbc
   conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ruta\a\bd.accdb;")
   print("Conexión exitosa")
   ```

### Logs de Depuración

Para habilitar logs detallados:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contacto y Soporte

Para reportar problemas o solicitar funcionalidades:
1. Revisar esta documentación
2. Verificar logs de error
3. Probar con base de datos de ejemplo
4. Documentar pasos para reproducir el problema