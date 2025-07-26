"""
Configuración y utilidades para el MCP Access Server.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

class AccessMCPConfig:
    """Configuración del servidor MCP Access."""
    
    # Configuración por defecto
    DEFAULT_CONFIG = {
        "server": {
            "name": "mcp-access-server",
            "version": "1.0.0",
            "description": "Servidor MCP para manipular bases de datos Microsoft Access"
        },
        "database": {
            "default_timeout": 30,
            "max_records_display": 50,
            "auto_commit": True
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "security": {
            "allow_drop_table": True,
            "allow_delete_records": True,
            "require_where_clause_for_updates": True
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Obtener la configuración actual."""
        return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def get_connection_string(cls, database_path: str, driver_type: str = "auto") -> str:
        """Generar cadena de conexión para Access."""
        
        if driver_type == "auto":
            if database_path.lower().endswith('.accdb'):
                driver = "Microsoft Access Driver (*.mdb, *.accdb)"
            else:
                driver = "Microsoft Access Driver (*.mdb)"
        else:
            driver = driver_type
        
        return f"DRIVER={{{driver}}};DBQ={database_path};"

class AccessDataTypes:
    """Tipos de datos soportados en Access."""
    
    TYPES = {
        "TEXT": "Texto corto (hasta 255 caracteres)",
        "MEMO": "Texto largo (hasta 65,535 caracteres)",
        "BYTE": "Número entero (0-255)",
        "INTEGER": "Número entero (-32,768 a 32,767)",
        "LONG": "Número entero largo (-2,147,483,648 a 2,147,483,647)",
        "SINGLE": "Número decimal de precisión simple",
        "DOUBLE": "Número decimal de precisión doble",
        "CURRENCY": "Moneda",
        "DATETIME": "Fecha y hora",
        "YESNO": "Sí/No (booleano)",
        "OLEOBJECT": "Objeto OLE",
        "HYPERLINK": "Hipervínculo",
        "AUTONUMBER": "Autonumérico"
    }
    
    @classmethod
    def get_type_info(cls, data_type: str) -> str:
        """Obtener información sobre un tipo de datos."""
        return cls.TYPES.get(data_type.upper(), "Tipo desconocido")
    
    @classmethod
    def list_types(cls) -> Dict[str, str]:
        """Listar todos los tipos disponibles."""
        return cls.TYPES.copy()

class QueryBuilder:
    """Constructor de consultas SQL para Access."""
    
    @staticmethod
    def select(table: str, columns: list = None, where: str = None, 
               order_by: str = None, limit: int = None) -> str:
        """Construir consulta SELECT."""
        
        # Columnas
        if columns:
            column_str = ", ".join(columns)
        else:
            column_str = "*"
        
        # Consulta base
        query = f"SELECT {column_str} FROM {table}"
        
        # WHERE
        if where:
            query += f" WHERE {where}"
        
        # ORDER BY
        if order_by:
            query += f" ORDER BY {order_by}"
        
        # LIMIT (TOP en Access)
        if limit:
            query = query.replace("SELECT", f"SELECT TOP {limit}")
        
        return query
    
    @staticmethod
    def insert(table: str, data: Dict[str, Any]) -> tuple:
        """Construir consulta INSERT."""
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ", ".join(["?" for _ in values])
        
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        return query, values
    
    @staticmethod
    def update(table: str, data: Dict[str, Any], where: str) -> tuple:
        """Construir consulta UPDATE."""
        set_clauses = [f"{col} = ?" for col in data.keys()]
        values = list(data.values())
        
        query = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {where}"
        return query, values
    
    @staticmethod
    def delete(table: str, where: str) -> str:
        """Construir consulta DELETE."""
        return f"DELETE FROM {table} WHERE {where}"
    
    @staticmethod
    def create_table(table: str, columns: list) -> str:
        """Construir consulta CREATE TABLE."""
        column_definitions = []
        
        for col in columns:
            col_def = f"{col['name']} {col['type']}"
            
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            if col.get('not_null'):
                col_def += " NOT NULL"
            if col.get('default'):
                col_def += f" DEFAULT {col['default']}"
            if col.get('auto_increment'):
                col_def += " AUTOINCREMENT"
                
            column_definitions.append(col_def)
        
        return f"CREATE TABLE {table} ({', '.join(column_definitions)})"

class AccessUtils:
    """Utilidades para trabajar con Access."""
    
    @staticmethod
    def validate_database_path(path: str) -> bool:
        """Validar que la ruta de la base de datos sea válida."""
        if not path:
            return False
        
        path_obj = Path(path)
        
        # Verificar que existe
        if not path_obj.exists():
            return False
        
        # Verificar extensión
        valid_extensions = ['.mdb', '.accdb']
        if path_obj.suffix.lower() not in valid_extensions:
            return False
        
        return True
    
    @staticmethod
    def format_results_table(results: list, max_width: int = 100) -> str:
        """Formatear resultados como tabla legible."""
        if not results:
            return "No hay resultados"
        
        # Obtener encabezados
        headers = list(results[0].keys())
        
        # Calcular anchos de columna
        col_widths = {}
        for header in headers:
            col_widths[header] = len(header)
            for row in results:
                value_str = str(row[header]) if row[header] is not None else "NULL"
                col_widths[header] = max(col_widths[header], len(value_str))
        
        # Ajustar anchos si es necesario
        total_width = sum(col_widths.values()) + len(headers) * 3 - 1
        if total_width > max_width:
            # Reducir anchos proporcionalmente
            reduction_factor = max_width / total_width
            for header in headers:
                col_widths[header] = max(8, int(col_widths[header] * reduction_factor))
        
        # Construir tabla
        result = ""
        
        # Encabezados
        header_row = " | ".join([header.ljust(col_widths[header]) for header in headers])
        result += header_row + "\n"
        
        # Separador
        separator = "-+-".join(["-" * col_widths[header] for header in headers])
        result += separator + "\n"
        
        # Datos
        for row in results:
            values = []
            for header in headers:
                value = row[header] if row[header] is not None else "NULL"
                value_str = str(value)
                if len(value_str) > col_widths[header]:
                    value_str = value_str[:col_widths[header]-3] + "..."
                values.append(value_str.ljust(col_widths[header]))
            
            result += " | ".join(values) + "\n"
        
        return result
    
    @staticmethod
    def escape_sql_identifier(identifier: str) -> str:
        """Escapar identificadores SQL (nombres de tabla, columna)."""
        # En Access, usar corchetes para escapar
        return f"[{identifier}]"
    
    @staticmethod
    def get_sample_queries() -> Dict[str, str]:
        """Obtener consultas de ejemplo."""
        return {
            "listar_tablas": "SELECT MSysObjects.Name FROM MSysObjects WHERE MSysObjects.Type=1 AND MSysObjects.Flags=0",
            "contar_registros": "SELECT COUNT(*) as total FROM {tabla}",
            "estructura_tabla": "SELECT * FROM {tabla} WHERE 1=0",
            "tablas_con_datos": """
                SELECT MSysObjects.Name, 
                       (SELECT COUNT(*) FROM [' + MSysObjects.Name + ']) as Registros
                FROM MSysObjects 
                WHERE MSysObjects.Type=1 AND MSysObjects.Flags=0
            """,
            "buscar_texto": "SELECT * FROM {tabla} WHERE {campo} LIKE '%{texto}%'",
            "registros_recientes": "SELECT TOP 10 * FROM {tabla} ORDER BY {campo_fecha} DESC"
        }

# Configuración global
CONFIG = AccessMCPConfig.get_config()