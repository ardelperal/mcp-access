#!/usr/bin/env python3
"""
Servidor MCP para manipular bases de datos de Microsoft Access.
Proporciona herramientas completas para gestionar tablas, consultas y datos.
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List, Optional, Sequence
import pyodbc
from pathlib import Path

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl
import mcp.types as types

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-access-server")

class AccessDatabaseManager:
    """Gestor de conexiones y operaciones con bases de datos Access."""
    
    def __init__(self):
        self.connection: Optional[pyodbc.Connection] = None
        self.database_path: Optional[str] = None
        
    def connect(self, database_path: str, password: str = "dpddpd") -> bool:
        """Conectar a una base de datos Access.
        
        Args:
            database_path: Ruta al archivo de base de datos
            password: Contraseña de la base de datos (por defecto: dpddpd)
        """
        # Determinar el driver apropiado
        if database_path.endswith('.accdb'):
            driver = "Microsoft Access Driver (*.mdb, *.accdb)"
        else:
            driver = "Microsoft Access Driver (*.mdb)"
        
        try:
            # Verificar que el archivo existe
            if not Path(database_path).exists():
                raise FileNotFoundError(f"La base de datos no existe: {database_path}")
            
            # Crear cadena de conexión con contraseña
            conn_str = f"DRIVER={{{driver}}};DBQ={database_path};"
            
            # Agregar contraseña si se proporciona
            if password:
                conn_str += f"PWD={password};"
            
            # Conectar
            self.connection = pyodbc.connect(conn_str)
            self.database_path = database_path
            logger.info(f"Conectado exitosamente a: {database_path} (con contraseña)")
            return True
            
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            # Si falla con contraseña, intentar sin contraseña
            if password:
                logger.info("Reintentando conexión sin contraseña...")
                try:
                    conn_str_no_pwd = f"DRIVER={{{driver}}};DBQ={database_path};"
                    self.connection = pyodbc.connect(conn_str_no_pwd)
                    self.database_path = database_path
                    logger.info(f"Conectado exitosamente a: {database_path} (sin contraseña)")
                    return True
                except Exception as e2:
                    logger.error(f"Error al conectar sin contraseña: {e2}")
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.database_path = None
            logger.info("Desconectado de la base de datos")
    
    def is_connected(self) -> bool:
        """Verificar si hay una conexión activa."""
        return self.connection is not None
    
    def execute_query(self, query: str, params: Optional[List] = None) -> List[Dict[str, Any]]:
        """Ejecutar una consulta SQL y retornar los resultados."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Si es una consulta SELECT, obtener resultados
            if query.strip().upper().startswith('SELECT'):
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                # Para INSERT, UPDATE, DELETE
                self.connection.commit()
                return [{"affected_rows": cursor.rowcount}]
                
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            raise
    
    def list_tables(self) -> List[str]:
        """Listar todas las tablas en la base de datos."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            cursor = self.connection.cursor()
            tables = []
            for table_info in cursor.tables(tableType='TABLE'):
                tables.append(table_info.table_name)
            return tables
        except Exception as e:
            logger.error(f"Error listando tablas: {e}")
            raise
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtener el esquema de una tabla específica."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            cursor = self.connection.cursor()
            columns = []
            for column in cursor.columns(table=table_name):
                columns.append({
                    "column_name": column.column_name,
                    "data_type": column.type_name,
                    "size": column.column_size,
                    "nullable": column.nullable == 1,
                    "default_value": column.column_def
                })
            return columns
        except Exception as e:
            logger.error(f"Error obteniendo esquema de tabla {table_name}: {e}")
            raise
    
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> bool:
        """Crear una nueva tabla."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            # Construir la consulta CREATE TABLE
            column_definitions = []
            for col in columns:
                col_def = f"{col['name']} {col['type']}"
                if col.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if col.get('not_null'):
                    col_def += " NOT NULL"
                if col.get('default'):
                    col_def += f" DEFAULT {col['default']}"
                column_definitions.append(col_def)
            
            query = f"CREATE TABLE {table_name} ({', '.join(column_definitions)})"
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            logger.info(f"Tabla {table_name} creada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error creando tabla {table_name}: {e}")
            raise
    
    def drop_table(self, table_name: str) -> bool:
        """Eliminar una tabla."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DROP TABLE {table_name}")
            self.connection.commit()
            logger.info(f"Tabla {table_name} eliminada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando tabla {table_name}: {e}")
            raise

# Instancia global del gestor de base de datos
db_manager = AccessDatabaseManager()

# Crear el servidor MCP
server = Server("mcp-access-server")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Listar todas las herramientas disponibles."""
    return [
        Tool(
            name="connect_database",
            description="Conectar a una base de datos Microsoft Access",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_path": {
                        "type": "string",
                        "description": "Ruta completa al archivo de base de datos Access (.mdb o .accdb)"
                    },
                    "password": {
                        "type": "string",
                        "description": "Contraseña de la base de datos (opcional, por defecto: dpddpd)"
                    }
                },
                "required": ["database_path"]
            }
        ),
        Tool(
            name="disconnect_database",
            description="Desconectar de la base de datos actual",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_tables",
            description="Listar todas las tablas en la base de datos conectada",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_table_schema",
            description="Obtener el esquema (estructura) de una tabla específica",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de la tabla"
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="create_table",
            description="Crear una nueva tabla en la base de datos",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de la nueva tabla"
                    },
                    "columns": {
                        "type": "array",
                        "description": "Lista de columnas con sus definiciones",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Nombre de la columna"},
                                "type": {"type": "string", "description": "Tipo de datos (TEXT, INTEGER, DOUBLE, DATE, etc.)"},
                                "primary_key": {"type": "boolean", "description": "Si es clave primaria"},
                                "not_null": {"type": "boolean", "description": "Si no permite valores nulos"},
                                "default": {"type": "string", "description": "Valor por defecto"}
                            },
                            "required": ["name", "type"]
                        }
                    }
                },
                "required": ["table_name", "columns"]
            }
        ),
        Tool(
            name="drop_table",
            description="Eliminar una tabla de la base de datos",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de la tabla a eliminar"
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="execute_query",
            description="Ejecutar una consulta SQL personalizada",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta SQL a ejecutar"
                    },
                    "parameters": {
                        "type": "array",
                        "description": "Parámetros para la consulta (opcional)",
                        "items": {"type": "string"}
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="insert_record",
            description="Insertar un nuevo registro en una tabla",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de la tabla"
                    },
                    "data": {
                        "type": "object",
                        "description": "Datos a insertar (clave: valor)"
                    }
                },
                "required": ["table_name", "data"]
            }
        ),
        Tool(
            name="update_record",
            description="Actualizar registros en una tabla",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de la tabla"
                    },
                    "data": {
                        "type": "object",
                        "description": "Datos a actualizar (clave: valor)"
                    },
                    "where_clause": {
                        "type": "string",
                        "description": "Condición WHERE para la actualización"
                    }
                },
                "required": ["table_name", "data", "where_clause"]
            }
        ),
        Tool(
            name="delete_record",
            description="Eliminar registros de una tabla",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de la tabla"
                    },
                    "where_clause": {
                        "type": "string",
                        "description": "Condición WHERE para la eliminación"
                    }
                },
                "required": ["table_name", "where_clause"]
            }
        ),
        Tool(
            name="get_records",
            description="Obtener registros de una tabla con filtros opcionales",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de la tabla"
                    },
                    "columns": {
                        "type": "array",
                        "description": "Columnas a seleccionar (opcional, por defecto todas)",
                        "items": {"type": "string"}
                    },
                    "where_clause": {
                        "type": "string",
                        "description": "Condición WHERE (opcional)"
                    },
                    "order_by": {
                        "type": "string",
                        "description": "Orden de los resultados (opcional)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Límite de registros (opcional)"
                    }
                },
                "required": ["table_name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Manejar las llamadas a las herramientas."""
    
    try:
        if name == "connect_database":
            database_path = arguments["database_path"]
            password = arguments.get("password", "dpddpd")  # Usar contraseña por defecto si no se proporciona
            success = db_manager.connect(database_path, password)
            if success:
                return [types.TextContent(
                    type="text",
                    text=f"✅ Conectado exitosamente a la base de datos: {database_path}"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text="❌ Error al conectar a la base de datos. Verifica la ruta, contraseña y que tengas los drivers de Access instalados."
                )]
        
        elif name == "disconnect_database":
            db_manager.disconnect()
            return [types.TextContent(
                type="text",
                text="✅ Desconectado de la base de datos"
            )]
        
        elif name == "list_tables":
            tables = db_manager.list_tables()
            if tables:
                table_list = "\n".join([f"• {table}" for table in tables])
                return [types.TextContent(
                    type="text",
                    text=f"📋 Tablas encontradas ({len(tables)}):\n{table_list}"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text="📋 No se encontraron tablas en la base de datos"
                )]
        
        elif name == "get_table_schema":
            table_name = arguments["table_name"]
            schema = db_manager.get_table_schema(table_name)
            if schema:
                schema_text = f"📊 Esquema de la tabla '{table_name}':\n\n"
                for col in schema:
                    nullable = "NULL" if col["nullable"] else "NOT NULL"
                    default = f" DEFAULT {col['default_value']}" if col["default_value"] else ""
                    schema_text += f"• {col['column_name']} - {col['data_type']}({col['size']}) {nullable}{default}\n"
                return [types.TextContent(type="text", text=schema_text)]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ No se pudo obtener el esquema de la tabla '{table_name}'"
                )]
        
        elif name == "create_table":
            table_name = arguments["table_name"]
            columns = arguments["columns"]
            success = db_manager.create_table(table_name, columns)
            if success:
                return [types.TextContent(
                    type="text",
                    text=f"✅ Tabla '{table_name}' creada exitosamente"
                )]
        
        elif name == "drop_table":
            table_name = arguments["table_name"]
            success = db_manager.drop_table(table_name)
            if success:
                return [types.TextContent(
                    type="text",
                    text=f"✅ Tabla '{table_name}' eliminada exitosamente"
                )]
        
        elif name == "execute_query":
            query = arguments["query"]
            parameters = arguments.get("parameters")
            results = db_manager.execute_query(query, parameters)
            
            if query.strip().upper().startswith('SELECT'):
                if results:
                    # Formatear resultados de SELECT
                    result_text = f"📊 Resultados de la consulta ({len(results)} registros):\n\n"
                    if len(results) > 0:
                        # Mostrar encabezados
                        headers = list(results[0].keys())
                        result_text += " | ".join(headers) + "\n"
                        result_text += "-" * (len(" | ".join(headers))) + "\n"
                        
                        # Mostrar datos (limitar a 50 registros para evitar overflow)
                        for i, row in enumerate(results[:50]):
                            values = [str(row[header]) if row[header] is not None else "NULL" for header in headers]
                            result_text += " | ".join(values) + "\n"
                        
                        if len(results) > 50:
                            result_text += f"\n... y {len(results) - 50} registros más"
                else:
                    result_text = "📊 La consulta no devolvió resultados"
            else:
                # Para INSERT, UPDATE, DELETE
                affected = results[0]["affected_rows"] if results else 0
                result_text = f"✅ Consulta ejecutada. Registros afectados: {affected}"
            
            return [types.TextContent(type="text", text=result_text)]
        
        elif name == "insert_record":
            table_name = arguments["table_name"]
            data = arguments["data"]
            
            # Construir consulta INSERT
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ", ".join(["?" for _ in values])
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            results = db_manager.execute_query(query, values)
            return [types.TextContent(
                type="text",
                text=f"✅ Registro insertado en '{table_name}'"
            )]
        
        elif name == "update_record":
            table_name = arguments["table_name"]
            data = arguments["data"]
            where_clause = arguments["where_clause"]
            
            # Construir consulta UPDATE
            set_clauses = [f"{col} = ?" for col in data.keys()]
            query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE {where_clause}"
            
            results = db_manager.execute_query(query, list(data.values()))
            affected = results[0]["affected_rows"] if results else 0
            return [types.TextContent(
                type="text",
                text=f"✅ Actualización completada en '{table_name}'. Registros afectados: {affected}"
            )]
        
        elif name == "delete_record":
            table_name = arguments["table_name"]
            where_clause = arguments["where_clause"]
            
            query = f"DELETE FROM {table_name} WHERE {where_clause}"
            results = db_manager.execute_query(query)
            affected = results[0]["affected_rows"] if results else 0
            return [types.TextContent(
                type="text",
                text=f"✅ Eliminación completada en '{table_name}'. Registros eliminados: {affected}"
            )]
        
        elif name == "get_records":
            table_name = arguments["table_name"]
            columns = arguments.get("columns", ["*"])
            where_clause = arguments.get("where_clause")
            order_by = arguments.get("order_by")
            limit = arguments.get("limit")
            
            # Construir consulta SELECT
            column_str = ", ".join(columns) if columns != ["*"] else "*"
            query = f"SELECT {column_str} FROM {table_name}"
            
            if where_clause:
                query += f" WHERE {where_clause}"
            if order_by:
                query += f" ORDER BY {order_by}"
            if limit:
                query += f" TOP {limit}"
            
            results = db_manager.execute_query(query)
            
            if results:
                result_text = f"📊 Registros de '{table_name}' ({len(results)} encontrados):\n\n"
                if len(results) > 0:
                    # Mostrar encabezados
                    headers = list(results[0].keys())
                    result_text += " | ".join(headers) + "\n"
                    result_text += "-" * (len(" | ".join(headers))) + "\n"
                    
                    # Mostrar datos
                    for row in results:
                        values = [str(row[header]) if row[header] is not None else "NULL" for header in headers]
                        result_text += " | ".join(values) + "\n"
            else:
                result_text = f"📊 No se encontraron registros en '{table_name}'"
            
            return [types.TextContent(type="text", text=result_text)]
        
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Herramienta desconocida: {name}"
            )]
    
    except Exception as e:
        error_msg = f"❌ Error ejecutando '{name}': {str(e)}"
        logger.error(error_msg)
        return [types.TextContent(type="text", text=error_msg)]

async def main():
    """Función principal para ejecutar el servidor MCP."""
    # Configurar opciones de inicialización
    init_options = InitializationOptions(
        server_name="mcp-access-server",
        server_version="1.0.0",
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={}
        )
    )
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            init_options
        )

if __name__ == "__main__":
    asyncio.run(main())