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

# COM automation imports
try:
    import win32com.client
    import pythoncom
    COM_AVAILABLE = True
except ImportError:
    COM_AVAILABLE = False
    logging.warning("pywin32 no está disponible. Funcionalidad COM deshabilitada.")

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

# Importar módulo de documentación mejorada
try:
    from .enhanced_documentation import EnhancedDocumentationGenerator
    ENHANCED_DOC_AVAILABLE = True
except ImportError:
    try:
        from enhanced_documentation import EnhancedDocumentationGenerator
        ENHANCED_DOC_AVAILABLE = True
    except ImportError:
        ENHANCED_DOC_AVAILABLE = False
        logging.warning("Módulo de documentación mejorada no disponible")

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
            
            try:
                # Intentar obtener información de columnas usando ODBC
                for column in cursor.columns(table=table_name):
                    columns.append({
                        "column_name": column.column_name,
                        "data_type": column.type_name,
                        "size": column.column_size,
                        "nullable": column.nullable == 1,
                        "default_value": column.column_def
                    })
            except UnicodeDecodeError as e:
                # Manejar errores de codificación específicamente
                logger.warning(f"Error de codificación en tabla {table_name}: {e}")
                # Usar método alternativo con consulta SQL directa
                try:
                    # Intentar obtener información básica de la tabla
                    query = f"SELECT TOP 1 * FROM [{table_name}]"
                    cursor.execute(query)
                    
                    # Obtener información de las columnas desde el cursor
                    for i, desc in enumerate(cursor.description):
                        col_name = desc[0] if desc[0] else f"Column_{i}"
                        col_type = self._map_type_code_to_name(desc[1]) if len(desc) > 1 else "TEXT"
                        col_size = desc[2] if len(desc) > 2 and desc[2] else 255
                        
                        columns.append({
                            "column_name": col_name,
                            "data_type": col_type,
                            "size": col_size,
                            "nullable": True,  # Valor por defecto
                            "default_value": None
                        })
                except Exception as inner_e:
                    logger.warning(f"No se pudo obtener esquema alternativo para {table_name}: {inner_e}")
                    # Crear esquema genérico
                    columns.append({
                        "column_name": "ID",
                        "data_type": "INTEGER",
                        "size": 4,
                        "nullable": False,
                        "default_value": None
                    })
            except Exception as e:
                logger.warning(f"Error general obteniendo esquema de {table_name}: {e}")
                # Crear esquema genérico
                columns.append({
                    "column_name": "ID",
                    "data_type": "INTEGER", 
                    "size": 4,
                    "nullable": False,
                    "default_value": None
                })
            
            return columns
            
        except Exception as e:
            logger.error(f"Error obteniendo esquema de tabla {table_name}: {e}")
            # Retornar esquema básico en lugar de lanzar excepción
            return [{
                "column_name": "ID",
                "data_type": "INTEGER",
                "size": 4,
                "nullable": False,
                "default_value": None
            }]
    
    def _map_type_code_to_name(self, type_code: int) -> str:
        """Mapear códigos de tipo ODBC a nombres de tipo."""
        type_mapping = {
            1: "CHAR",
            4: "INTEGER", 
            5: "SMALLINT",
            6: "FLOAT",
            7: "REAL",
            8: "DOUBLE",
            12: "VARCHAR",
            91: "DATE",
            92: "TIME",
            93: "TIMESTAMP",
            -1: "LONGVARCHAR",
            -2: "BINARY",
            -3: "VARBINARY",
            -4: "LONGVARBINARY"
        }
        return type_mapping.get(type_code, "TEXT")
    
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
    
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        """Obtener las relaciones entre tablas de la base de datos."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        relationships = []
        
        # Método 1: Intentar usar COM automation (más confiable)
        if COM_AVAILABLE and self.database_path:
            try:
                com_manager = AccessCOMManager()
                if com_manager.connect(self.database_path):
                    com_relationships = com_manager.get_relationships()
                    
                    for rel in com_relationships:
                        # Convertir formato COM a formato estándar
                        for field in rel.get('fields', []):
                            relationships.append({
                                "parent_table": rel['table'],
                                "parent_column": field['name'],
                                "child_table": rel['foreign_table'],
                                "child_column": field['foreign_name'],
                                "constraint_name": rel['name'],
                                "update_rule": "NO ACTION",
                                "delete_rule": "NO ACTION",
                                "detection_method": "COM_automation",
                                "confidence": "very_high"
                            })
                    
                    com_manager.disconnect()
                    
                    if relationships:
                        logger.info(f"Encontradas {len(relationships)} relaciones usando COM automation")
                        return relationships
                        
            except Exception as e:
                logger.debug(f"COM automation falló: {e}")
        
        # Método 2: ODBC foreignKeys (fallback)
        try:
            cursor = self.connection.cursor()
            
            try:
                # Intentar obtener información de claves foráneas usando ODBC
                for fk in cursor.foreignKeys():
                    relationships.append({
                        "parent_table": fk.pktable_name,
                        "parent_column": fk.pkcolumn_name,
                        "child_table": fk.fktable_name,
                        "child_column": fk.fkcolumn_name,
                        "constraint_name": fk.fk_name,
                        "update_rule": fk.update_rule,
                        "delete_rule": fk.delete_rule,
                        "detection_method": "ODBC_foreignKeys",
                        "confidence": "high"
                    })
                    
                if relationships:
                    logger.info(f"Encontradas {len(relationships)} relaciones usando ODBC foreignKeys")
                    return relationships
                    
            except Exception as e:
                logger.debug(f"ODBC foreignKeys falló: {e}")
                
            # Método 3: MSysRelationships (fallback)
            try:
                query = """
                SELECT DISTINCT 
                    MSysRelationships.szObject as ParentTable,
                    MSysRelationships.szColumn as ParentColumn,
                    MSysRelationships.szReferencedObject as ChildTable,
                    MSysRelationships.szReferencedColumn as ChildColumn,
                    MSysRelationships.szRelationship as ConstraintName
                FROM MSysRelationships
                """
                
                results = self.execute_query(query)
                for result in results:
                    relationships.append({
                        "parent_table": result.get('ParentTable', 'Unknown'),
                        "parent_column": result.get('ParentColumn', 'Unknown'),
                        "child_table": result.get('ChildTable', 'Unknown'),
                        "child_column": result.get('ChildColumn', 'Unknown'),
                        "constraint_name": result.get('ConstraintName', 'Unknown'),
                        "update_rule": "NO ACTION",
                        "delete_rule": "NO ACTION",
                        "detection_method": "MSysRelationships",
                        "confidence": "high"
                    })
                    
                if relationships:
                    logger.info(f"Encontradas {len(relationships)} relaciones usando MSysRelationships")
                    return relationships
                    
            except Exception as e:
                logger.debug(f"MSysRelationships no accesible: {e}")
            
        except Exception as e:
            logger.error(f"Error en métodos directos de relaciones: {e}")
        
        # Método 4: Inferencia avanzada (último recurso)
        logger.info("Usando métodos de inferencia para detectar relaciones")
        relationships.extend(self._infer_relationships_advanced())
        
        return relationships
    
    def _infer_relationships_advanced(self) -> List[Dict[str, Any]]:
        """Inferir relaciones usando múltiples técnicas avanzadas."""
        relationships = []
        tables = self.list_tables()
        
        # Método 1: Análisis por nombres de columnas (mejorado)
        relationships.extend(self._infer_by_column_names(tables))
        
        # Método 2: Análisis por patrones de datos
        relationships.extend(self._infer_by_data_patterns(tables))
        
        # Método 3: Análisis por índices
        relationships.extend(self._infer_by_indexes(tables))
        
        return relationships
    
    def _infer_by_column_names(self, tables: List[str]) -> List[Dict[str, Any]]:
        """Inferir relaciones basándose en nombres de columnas."""
        relationships = []
        
        for table in tables:
            try:
                schema = self.get_table_schema(table)
                for col in schema:
                    col_name = col['column_name']
                    col_upper = col_name.upper()
                    
                    # Patrones de claves foráneas
                    patterns = [
                        # Patrón: NombreTablaID
                        (lambda name: name.endswith('ID') and len(name) > 2, lambda name: name[:-2]),
                        # Patrón: ID_NombreTabla
                        (lambda name: name.startswith('ID_'), lambda name: name[3:]),
                        # Patrón: NombreTabla_ID
                        (lambda name: '_ID' in name, lambda name: name.split('_ID')[0]),
                        # Patrón: FK_NombreTabla
                        (lambda name: name.startswith('FK_'), lambda name: name[3:]),
                    ]
                    
                    for pattern_check, extract_table in patterns:
                        if pattern_check(col_upper) and col_upper != 'ID':
                            potential_parent = extract_table(col_upper)
                            
                            # Buscar tabla padre con coincidencia flexible
                            for parent_table in tables:
                                parent_upper = parent_table.upper()
                                if (parent_upper == potential_parent or 
                                    parent_upper.startswith(potential_parent) or
                                    potential_parent.startswith(parent_upper.split('_')[0])):
                                    
                                    relationships.append({
                                        "parent_table": parent_table,
                                        "parent_column": "ID",
                                        "child_table": table,
                                        "child_column": col_name,
                                        "constraint_name": f"FK_{table}_{col_name}",
                                        "update_rule": "NO ACTION",
                                        "delete_rule": "NO ACTION",
                                        "detection_method": "column_name_inference",
                                        "confidence": "medium"
                                    })
                                    break
            except Exception:
                continue
        
        return relationships
    
    def _infer_by_data_patterns(self, tables: List[str]) -> List[Dict[str, Any]]:
        """Inferir relaciones analizando patrones en los datos."""
        relationships = []
        
        for table in tables:
            try:
                schema = self.get_table_schema(table)
                for col in schema:
                    col_name = col['column_name']
                    
                    # Solo analizar columnas numéricas que podrían ser claves foráneas
                    if col['data_type'] in ['INTEGER', 'LONG', 'DOUBLE'] and col_name.upper() != 'ID':
                        # Obtener valores únicos de la columna
                        try:
                            query = f"SELECT DISTINCT TOP 10 [{col_name}] FROM [{table}] WHERE [{col_name}] IS NOT NULL"
                            results = self.execute_query(query)
                            
                            if results and len(results) > 0:
                                values = [str(r[col_name]) for r in results if r[col_name] is not None]
                                
                                # Buscar si estos valores existen como IDs en otras tablas
                                for potential_parent in tables:
                                    if potential_parent != table:
                                        try:
                                            # Verificar si los valores existen en la tabla padre
                                            check_query = f"SELECT COUNT(*) as count FROM [{potential_parent}] WHERE [ID] IN ({','.join(values[:5])})"
                                            check_result = self.execute_query(check_query)
                                            
                                            if check_result and check_result[0]['count'] > 0:
                                                relationships.append({
                                                    "parent_table": potential_parent,
                                                    "parent_column": "ID",
                                                    "child_table": table,
                                                    "child_column": col_name,
                                                    "constraint_name": f"FK_{table}_{col_name}_inferred",
                                                    "update_rule": "NO ACTION",
                                                    "delete_rule": "NO ACTION",
                                                    "detection_method": "data_pattern_analysis",
                                                    "confidence": "high"
                                                })
                                                break
                                        except Exception:
                                            continue
                        except Exception:
                            continue
            except Exception:
                continue
        
        return relationships
    
    def _infer_by_indexes(self, tables: List[str]) -> List[Dict[str, Any]]:
        """Inferir relaciones basándose en índices."""
        relationships = []
        
        for table in tables:
            try:
                indexes = self.get_table_indexes(table)
                for idx in indexes:
                    # Buscar índices que podrían ser claves foráneas
                    if not idx.get('unique', False) and idx.get('type') != 'PRIMARY':
                        columns = idx.get('columns', [idx.get('column_name', '')])
                        
                        for col_name in columns:
                            if col_name and col_name.upper().endswith('ID') and col_name.upper() != 'ID':
                                # Buscar tabla padre potencial
                                potential_parent = col_name[:-2]
                                for parent_table in tables:
                                    if parent_table.upper().startswith(potential_parent.upper()):
                                        relationships.append({
                                            "parent_table": parent_table,
                                            "parent_column": "ID",
                                            "child_table": table,
                                            "child_column": col_name,
                                            "constraint_name": f"FK_{table}_{col_name}_idx",
                                            "update_rule": "NO ACTION",
                                            "delete_rule": "NO ACTION",
                                            "detection_method": "index_analysis",
                                            "confidence": "medium"
                                        })
                                        break
            except Exception:
                continue
        
        return relationships
    
    def get_table_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtener los índices de una tabla específica."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            cursor = self.connection.cursor()
            indexes = []
            
            # Primero intentar usar la función statistics de ODBC
            try:
                stats_found = False
                for index in cursor.statistics(table=table_name):
                    if index.index_name:  # Filtrar entradas sin nombre de índice
                        stats_found = True
                        # Agrupar columnas por índice
                        existing_index = None
                        for idx in indexes:
                            if idx["index_name"] == index.index_name:
                                existing_index = idx
                                break
                        
                        if existing_index:
                            existing_index["columns"].append(index.column_name)
                        else:
                            indexes.append({
                                "index_name": index.index_name,
                                "columns": [index.column_name],
                                "unique": not index.non_unique,
                                "ordinal_position": index.ordinal_position,
                                "type": "INDEX"
                            })
                
                if stats_found:
                    return indexes
                    
            except Exception as e:
                logger.debug(f"Función statistics no disponible para {table_name}: {e}")
            
            # Si statistics no funciona, intentar método alternativo más simple
            # Crear índices genéricos basados en el esquema de la tabla
            try:
                schema = self.get_table_schema(table_name)
                primary_keys = []
                
                # Buscar posibles claves primarias
                for col in schema:
                    col_name = col['column_name'].upper()
                    if col_name == 'ID' or (col_name.endswith('ID') and len(col_name) <= 10):
                        primary_keys.append(col['column_name'])
                
                # Crear índice para clave primaria si se encontró
                if primary_keys:
                    indexes.append({
                        "index_name": "PrimaryKey",
                        "columns": primary_keys[:1],  # Solo tomar el primero
                        "unique": True,
                        "ordinal_position": 1,
                        "type": "PRIMARY"
                    })
                
                # Crear índices genéricos para otras columnas importantes
                for i, col in enumerate(schema[:5]):  # Solo primeras 5 columnas
                    col_name = col['column_name']
                    if col_name not in primary_keys:
                        indexes.append({
                            "index_name": f"Index_{col_name}",
                            "columns": [col_name],
                            "unique": False,
                            "ordinal_position": i + 2,
                            "type": "INDEX"
                        })
                
            except Exception as e:
                logger.debug(f"Error creando índices genéricos para {table_name}: {e}")
                # Como último recurso, crear un índice básico
                indexes.append({
                    "index_name": "PrimaryKey",
                    "columns": ["ID"],
                    "unique": True,
                    "ordinal_position": 1,
                    "type": "PRIMARY"
                })
            
            return indexes
            
        except Exception as e:
            logger.warning(f"Error obteniendo índices de tabla {table_name}: {e}")
            # Retornar lista con índice básico en lugar de lista vacía
            return [{
                "index_name": "PrimaryKey",
                "columns": ["ID"],
                "unique": True,
                "ordinal_position": 1,
                "type": "PRIMARY"
            }]
    
    def get_primary_keys(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtener las claves primarias de una tabla."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            cursor = self.connection.cursor()
            primary_keys = []
            
            # Intentar usar cursor.primaryKeys primero
            try:
                for pk in cursor.primaryKeys(table=table_name):
                    primary_keys.append({
                        "column_name": pk.column_name,
                        "table_name": table_name,
                        "constraint_name": pk.pk_name or "PRIMARY_KEY"
                    })
                
                if primary_keys:
                    return primary_keys
                    
            except Exception as e:
                logger.debug(f"Método primaryKeys no disponible para {table_name}: {e}")
            
            # Método alternativo: buscar columnas que probablemente sean claves primarias
            try:
                schema = self.get_table_schema(table_name)
                for col in schema:
                    col_name = col['column_name'].upper()
                    # Buscar columnas comunes de clave primaria
                    if (col_name == 'ID' or 
                        col_name == f'{table_name.upper()}_ID' or
                        (col_name.endswith('ID') and len(col_name) <= 15)):
                        primary_keys.append({
                            "column_name": col['column_name'],
                            "table_name": table_name,
                            "constraint_name": "PRIMARY_KEY"
                        })
                        break  # Solo tomar la primera que encontremos
                
                # Si no encontramos ninguna, usar la primera columna como fallback
                if not primary_keys and schema:
                    primary_keys.append({
                        "column_name": schema[0]['column_name'],
                        "table_name": table_name,
                        "constraint_name": "PRIMARY_KEY"
                    })
                    
            except Exception as e:
                logger.debug(f"Error analizando esquema para claves primarias en {table_name}: {e}")
            
            return primary_keys
            
        except Exception as e:
            logger.warning(f"Error obteniendo claves primarias de tabla {table_name}: {e}")
            # Retornar lista con clave primaria genérica
            return [{
                "column_name": "ID",
                "table_name": table_name,
                "constraint_name": "PRIMARY_KEY"
            }]
    
    def generate_database_documentation(self) -> Dict[str, Any]:
        """Generar documentación completa de la base de datos."""
        if not self.is_connected():
            raise Exception("No hay conexión activa a la base de datos")
        
        try:
            documentation = {
                "database_path": self.database_path,
                "tables": {},
                "relationships": [],
                "summary": {}
            }
            
            # Obtener todas las tablas
            tables = self.list_tables()
            documentation["summary"]["total_tables"] = len(tables)
            
            # Documentar cada tabla
            for table in tables:
                table_doc = {
                    "schema": self.get_table_schema(table),
                    "primary_keys": self.get_primary_keys(table),
                    "indexes": self.get_table_indexes(table),
                    "record_count": 0
                }
                
                # Obtener conteo de registros
                try:
                    count_result = self.execute_query(f"SELECT COUNT(*) as count FROM [{table}]")
                    table_doc["record_count"] = count_result[0]["count"] if count_result else 0
                except:
                    table_doc["record_count"] = "N/A"
                
                documentation["tables"][table] = table_doc
            
            # Obtener relaciones con análisis detallado
            relationships = self.get_table_relationships()
            documentation["relationships"] = relationships
            documentation["summary"]["total_relationships"] = len(relationships)
            
            # Agrupar relaciones por tabla para análisis
            table_relationships = {}
            detection_stats = {}
            confidence_stats = {}
            
            for rel in relationships:
                parent = rel['parent_table']
                child = rel['child_table']
                method = rel.get('detection_method', 'unknown')
                confidence = rel.get('confidence', 'unknown')
                
                # Agrupar por tabla
                if parent not in table_relationships:
                    table_relationships[parent] = {'as_parent': [], 'as_child': []}
                if child not in table_relationships:
                    table_relationships[child] = {'as_parent': [], 'as_child': []}
                
                table_relationships[parent]['as_parent'].append(rel)
                table_relationships[child]['as_child'].append(rel)
                
                # Estadísticas de métodos de detección
                detection_stats[method] = detection_stats.get(method, 0) + 1
                
                # Estadísticas de confianza
                if confidence != 'unknown':
                    confidence_stats[confidence] = confidence_stats.get(confidence, 0) + 1
            
            # Agregar relaciones por tabla a la documentación
            for table in tables:
                if table in table_relationships:
                    documentation["tables"][table]["relationships"] = table_relationships[table]
                else:
                    documentation["tables"][table]["relationships"] = {'as_parent': [], 'as_child': []}
            
            # Agregar estadísticas de relaciones
            documentation["summary"]["relationship_detection_methods"] = detection_stats
            documentation["summary"]["relationship_confidence_levels"] = confidence_stats
            
            return documentation
            
        except Exception as e:
            logger.error(f"Error generando documentación: {e}")
            raise
    
    def export_documentation_markdown(self) -> str:
        """Exportar la documentación en formato Markdown."""
        doc = self.generate_database_documentation()
        
        markdown = f"""# Documentación de Base de Datos

**Archivo:** `{doc['database_path']}`  
**Fecha de generación:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Resumen

- **Total de tablas:** {doc['summary']['total_tables']}
- **Total de relaciones:** {doc['summary']['total_relationships']}

## Tablas

"""
        
        # Documentar cada tabla
        for table_name, table_info in doc["tables"].items():
            markdown += f"""### {table_name}

**Registros:** {table_info['record_count']}

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
"""
            
            for col in table_info["schema"]:
                nullable = "Sí" if col["nullable"] else "No"
                default = col["default_value"] if col["default_value"] else "-"
                markdown += f"| {col['column_name']} | {col['data_type']} | {col['size']} | {nullable} | {default} |\n"
            
            # Claves primarias
            if table_info["primary_keys"]:
                pk_names = [pk['column_name'] if isinstance(pk, dict) else str(pk) for pk in table_info['primary_keys']]
                markdown += f"\n**Claves Primarias:** {', '.join(pk_names)}\n"
            
            # Índices
            if table_info["indexes"]:
                markdown += "\n#### Índices\n"
                for idx in table_info["indexes"]:
                    unique_text = " (ÚNICO)" if idx["unique"] else ""
                    # Manejar tanto el formato nuevo (columns) como el viejo (column_name)
                    if "columns" in idx:
                        columns_str = ", ".join(idx["columns"])
                    else:
                        columns_str = idx.get("column_name", "N/A")
                    markdown += f"- **{idx['index_name']}**: {columns_str}{unique_text}\n"
            
            markdown += "\n---\n\n"
        
        # Relaciones
        if doc["relationships"]:
            markdown += "## Relaciones entre Tablas\n\n"
            
            # Estadísticas de métodos de detección
            if "relationship_detection_methods" in doc["summary"]:
                markdown += "### Métodos de Detección Utilizados\n\n"
                for method, count in doc["summary"]["relationship_detection_methods"].items():
                    method_names = {
                        "ODBC_foreignKeys": "ODBC Foreign Keys",
                        "MSysRelationships": "Tablas del Sistema Access",
                        "column_name_inference": "Inferencia por Nombres de Columnas",
                        "data_pattern_analysis": "Análisis de Patrones de Datos",
                        "index_analysis": "Análisis de Índices"
                    }
                    method_display = method_names.get(method, method)
                    markdown += f"- **{method_display}**: {count} relaciones\n"
                markdown += "\n"
            
            # Estadísticas de confianza
            if "relationship_confidence_levels" in doc["summary"] and doc["summary"]["relationship_confidence_levels"]:
                markdown += "### Niveles de Confianza\n\n"
                for confidence, count in doc["summary"]["relationship_confidence_levels"].items():
                    confidence_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(confidence, "⚪")
                    markdown += f"- {confidence_emoji} **{confidence.title()}**: {count} relaciones\n"
                markdown += "\n"
            
            markdown += "### Lista de Relaciones\n\n"
            for rel in doc["relationships"]:
                # Emoji según método de detección
                method_emoji = {
                    "ODBC_foreignKeys": "🔗",
                    "MSysRelationships": "🏛️",
                    "column_name_inference": "🔤",
                    "data_pattern_analysis": "📊",
                    "index_analysis": "📇"
                }.get(rel.get('detection_method', ''), "❓")
                
                # Emoji según confianza
                confidence_emoji = {
                    "high": "🟢",
                    "medium": "🟡", 
                    "low": "🔴"
                }.get(rel.get('confidence', ''), "")
                
                markdown += f"{method_emoji} **{rel['parent_table']}.{rel['parent_column']}** → **{rel['child_table']}.{rel['child_column']}** {confidence_emoji}\n"
                
                if rel["constraint_name"]:
                    markdown += f"  - Restricción: `{rel['constraint_name']}`\n"
                
                markdown += f"  - Actualización: {rel['update_rule']}, Eliminación: {rel['delete_rule']}\n"
                
                # Mostrar método de detección y confianza
                method_display = {
                    "ODBC_foreignKeys": "ODBC Foreign Keys",
                    "MSysRelationships": "Tablas del Sistema",
                    "column_name_inference": "Inferencia por Nombres",
                    "data_pattern_analysis": "Análisis de Datos",
                    "index_analysis": "Análisis de Índices"
                }.get(rel.get('detection_method', ''), rel.get('detection_method', 'Desconocido'))
                
                markdown += f"  - Método: {method_display}"
                if rel.get('confidence'):
                    markdown += f", Confianza: {rel['confidence']}"
                markdown += "\n\n"
        
        # Agregar sección de relaciones por tabla
        if doc["relationships"]:
            markdown += "## Relaciones por Tabla\n\n"
            for table_name, table_info in doc["tables"].items():
                if "relationships" in table_info:
                    parent_rels = table_info["relationships"]["as_parent"]
                    child_rels = table_info["relationships"]["as_child"]
                    
                    if parent_rels or child_rels:
                        markdown += f"### {table_name}\n\n"
                        
                        if parent_rels:
                            markdown += "**Como tabla padre:**\n"
                            for rel in parent_rels:
                                markdown += f"- Referenciada por `{rel['child_table']}.{rel['child_column']}`\n"
                            markdown += "\n"
                        
                        if child_rels:
                            markdown += "**Como tabla hija:**\n"
                            for rel in child_rels:
                                markdown += f"- Referencia a `{rel['parent_table']}.{rel['parent_column']}`\n"
                            markdown += "\n"
        
        return markdown


class AccessCOMManager:
    """
    Gestor de base de datos Access usando COM automation.
    Proporciona acceso directo a las relaciones y metadatos de Access.
    """
    
    def __init__(self):
        self.access_app = None
        self.database = None
        self.db_path = None
        
    def connect(self, db_path: str, password: str = None) -> bool:
        """
        Conectar a una base de datos Access usando COM.
        
        Args:
            db_path: Ruta al archivo de base de datos
            password: Contraseña de la base de datos (opcional)
            
        Returns:
            bool: True si la conexión fue exitosa
        """
        if not COM_AVAILABLE:
            logging.error("COM automation no está disponible. Instale pywin32.")
            return False
            
        try:
            # Inicializar COM
            pythoncom.CoInitialize()
            
            # Crear instancia de Access con configuración silenciosa
            self.access_app = win32com.client.Dispatch("Access.Application")
            
            # Configuración ULTRA-AGRESIVA para modo completamente oculto
            self.access_app.Visible = False
            self.access_app.UserControl = False
            
            # Configurar seguridad de automatización al mínimo
            try:
                self.access_app.AutomationSecurity = 1  # msoAutomationSecurityLow
            except:
                pass
            
            # Desactivar TODAS las alertas, confirmaciones y diálogos
            try:
                self.access_app.DoCmd.SetWarnings(False)
                self.access_app.DisplayAlerts = False
            except:
                pass
            
            # Configurar TODAS las opciones para evitar cualquier diálogo
            try:
                # Confirmaciones
                self.access_app.SetOption("Confirm Action Queries", False)
                self.access_app.SetOption("Confirm Document Deletions", False)
                self.access_app.SetOption("Confirm Record Changes", False)
                self.access_app.SetOption("Confirm Append Queries", False)
                self.access_app.SetOption("Confirm Update Queries", False)
                self.access_app.SetOption("Confirm Delete Queries", False)
                
                # Diálogos de inicio y estado
                self.access_app.SetOption("Show Status Bar", False)
                self.access_app.SetOption("Show Startup Dialog Box", False)
                self.access_app.SetOption("Show Built-in Toolbars", False)
                
                # Errores y advertencias
                self.access_app.SetOption("Show Error Alerts", False)
                self.access_app.SetOption("Show Macro Error Dialog", False)
                
                # Configuraciones adicionales para automatización
                self.access_app.SetOption("Use Access Special Keys", False)
                self.access_app.SetOption("Allow Full Menus", False)
                self.access_app.SetOption("Allow Default Shortcut Menus", False)
            except Exception as e:
                logging.debug(f"Algunas opciones no se pudieron configurar: {e}")
            
            # Configuración adicional para evitar diálogos de contraseña
            try:
                # Intentar configurar el modo de error silencioso
                self.access_app.Application.SetOption("Error Checking", False)
            except:
                pass
            
            # Abrir la base de datos con estrategia COMPLETAMENTE SILENCIOSA
            # Usar solo DBEngine para evitar cualquier diálogo de Access
            try:
                # Obtener DBEngine antes de intentar abrir cualquier base de datos
                db_engine = self.access_app.DBEngine
                workspace = db_engine.Workspaces(0)
                
                # Estrategia: Probar primero con DBEngine (completamente silencioso)
                connection_string = ""
                if password:
                    connection_string = f";PWD={password}"
                
                try:
                    # Intentar abrir con DBEngine primero - esto NO muestra diálogos
                    test_db = workspace.OpenDatabase(db_path, False, False, connection_string)
                    test_db.Close()
                    
                    # Si llegamos aquí, la conexión es válida
                    # Ahora abrir con Access Application
                    if password:
                        self.access_app.OpenCurrentDatabase(db_path, False, password)
                    else:
                        self.access_app.OpenCurrentDatabase(db_path, False)
                        
                except Exception as db_engine_error:
                    # Analizar el error de DBEngine (sin diálogos)
                    error_msg = str(db_engine_error).lower()
                    
                    if password:
                        # Si se proporcionó contraseña pero falló
                        if any(keyword in error_msg for keyword in ["password", "contraseña", "invalid", "not a valid", "cannot open"]):
                            logging.error("Contraseña incorrecta o base de datos corrupta")
                            raise Exception("Contraseña incorrecta o la base de datos no se puede abrir.")
                        else:
                            logging.error(f"Error inesperado con contraseña: {db_engine_error}")
                            raise Exception(f"Error abriendo la base de datos: {db_engine_error}")
                    else:
                        # Si no se proporcionó contraseña
                        if any(keyword in error_msg for keyword in ["password", "contraseña", "invalid", "not a valid", "cannot open"]):
                            logging.warning("La base de datos requiere contraseña")
                            raise Exception("Base de datos protegida con contraseña. Proporcione la contraseña.")
                        else:
                            logging.error(f"Error inesperado sin contraseña: {db_engine_error}")
                            raise Exception(f"Error abriendo la base de datos: {db_engine_error}")
                
                # Verificar que la base de datos se abrió correctamente
                self.database = self.access_app.CurrentDb()
                if not self.database:
                    raise Exception("No se pudo obtener referencia a la base de datos")
                    
            except Exception as e:
                logging.error(f"Error abriendo base de datos: {e}")
                raise e
            
            self.db_path = db_path
            logging.info(f"Conectado a {db_path} usando COM")
            return True
            
        except Exception as e:
            logging.error(f"Error conectando con COM: {e}")
            self.disconnect()
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos y cerrar Access."""
        try:
            if self.access_app:
                # Restaurar configuraciones antes de cerrar
                try:
                    self.access_app.DoCmd.SetWarnings(True)
                except:
                    # Intentar restaurar con sintaxis alternativa
                    try:
                        self.access_app.Application.SetOption("Confirm Action Queries", True)
                        self.access_app.Application.SetOption("Confirm Document Deletions", True)
                        self.access_app.Application.SetOption("Confirm Record Changes", True)
                    except:
                        pass
                
                # Cerrar base de datos actual
                try:
                    self.access_app.CloseCurrentDatabase()
                except:
                    pass
                
                # Cerrar Access
                try:
                    self.access_app.Quit()
                except:
                    pass
                    
                self.access_app = None
                
            self.database = None
            self.db_path = None
            
            # Limpiar COM
            try:
                pythoncom.CoUninitialize()
            except:
                pass
            
        except Exception as e:
            logging.error(f"Error desconectando COM: {e}")
    
    def is_connected(self) -> bool:
        """Verificar si hay una conexión activa."""
        return self.access_app is not None and self.database is not None
    
    def get_relationships(self) -> List[Dict[str, Any]]:
        """
        Obtener todas las relaciones definidas en la base de datos usando COM.
        
        Returns:
            List[Dict]: Lista de relaciones con detalles completos
        """
        if not self.is_connected():
            return []
            
        relationships = []
        
        try:
            # Acceder a la colección de relaciones
            relations = self.database.Relations
            
            for i in range(relations.Count):
                relation = relations.Item(i)
                
                # Obtener información básica de la relación
                rel_info = {
                    'name': relation.Name,
                    'table': relation.Table,
                    'foreign_table': relation.ForeignTable,
                    'attributes': relation.Attributes,
                    'fields': []
                }
                
                # Obtener los campos de la relación
                fields = relation.Fields
                for j in range(fields.Count):
                    field = fields.Item(j)
                    field_info = {
                        'name': field.Name,
                        'foreign_name': field.ForeignName
                    }
                    rel_info['fields'].append(field_info)
                
                relationships.append(rel_info)
                
        except Exception as e:
            logging.error(f"Error obteniendo relaciones COM: {e}")
            
        return relationships
    
    def get_table_names(self) -> List[str]:
        """
        Obtener lista de nombres de tablas usando COM.
        
        Returns:
            List[str]: Lista de nombres de tablas
        """
        if not self.is_connected():
            return []
            
        table_names = []
        
        try:
            tabledefs = self.database.TableDefs
            
            for i in range(tabledefs.Count):
                tabledef = tabledefs.Item(i)
                # Filtrar tablas del sistema
                if not tabledef.Name.startswith("MSys"):
                    table_names.append(tabledef.Name)
                    
        except Exception as e:
            logging.error(f"Error obteniendo tablas COM: {e}")
            
        return table_names
    
    def get_table_fields(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Obtener información de campos de una tabla usando COM.
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            List[Dict]: Lista de campos con sus propiedades
        """
        if not self.is_connected():
            return []
            
        fields = []
        
        try:
            tabledef = self.database.TableDefs.Item(table_name)
            table_fields = tabledef.Fields
            
            for i in range(table_fields.Count):
                field = table_fields.Item(i)
                
                field_info = {
                    'name': field.Name,
                    'type': field.Type,
                    'size': field.Size,
                    'required': field.Required,
                    'allow_zero_length': getattr(field, 'AllowZeroLength', False)
                }
                
                fields.append(field_info)
                
        except Exception as e:
            logging.error(f"Error obteniendo campos COM para {table_name}: {e}")
            
        return fields
    
    def get_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Obtener información de índices de una tabla usando COM.
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            List[Dict]: Lista de índices con sus propiedades
        """
        if not self.is_connected():
            return []
            
        indexes = []
        
        try:
            tabledef = self.database.TableDefs.Item(table_name)
            table_indexes = tabledef.Indexes
            
            for i in range(table_indexes.Count):
                index = table_indexes.Item(i)
                
                index_info = {
                    'name': index.Name,
                    'primary': index.Primary,
                    'unique': index.Unique,
                    'foreign': index.Foreign,
                    'fields': []
                }
                
                # Obtener campos del índice
                index_fields = index.Fields
                for j in range(index_fields.Count):
                    field = index_fields.Item(j)
                    index_info['fields'].append(field.Name)
                
                indexes.append(index_info)
                
        except Exception as e:
            logging.error(f"Error obteniendo índices COM para {table_name}: {e}")
            
        return indexes


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
        ),
        Tool(
            name="get_table_relationships",
            description="Obtener las relaciones entre tablas de la base de datos",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_table_indexes",
            description="Obtener los índices de una tabla específica",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Nombre de la tabla"}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="get_primary_keys",
            description="Obtener las claves primarias de una tabla",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Nombre de la tabla"}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="generate_database_documentation",
            description="Generar documentación completa de la base de datos",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="export_documentation_markdown",
            description="Exportar la documentación de la base de datos en formato Markdown",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="generate_enhanced_documentation",
            description="Generar documentación mejorada con diagramas ER, análisis de calidad y múltiples formatos",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_er_diagram": {
                        "type": "boolean",
                        "description": "Incluir diagrama ER en formato Mermaid (por defecto: true)"
                    },
                    "include_data_quality": {
                        "type": "boolean", 
                        "description": "Incluir análisis de calidad de datos (por defecto: true)"
                    },
                    "include_field_analysis": {
                        "type": "boolean",
                        "description": "Incluir análisis detallado de campos (por defecto: true)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="export_documentation_html",
            description="Exportar documentación en formato HTML con estilos mejorados",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_path": {
                        "type": "string",
                        "description": "Ruta donde guardar el archivo HTML (opcional)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="export_documentation_json",
            description="Exportar documentación en formato JSON estructurado",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_path": {
                        "type": "string",
                        "description": "Ruta donde guardar el archivo JSON (opcional)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="analyze_data_quality",
            description="Realizar análisis de calidad de datos en todas las tablas",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Nombre de tabla específica (opcional, por defecto analiza todas)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="generate_er_diagram",
            description="Generar diagrama ER en formato Mermaid",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_path": {
                        "type": "string",
                        "description": "Ruta donde guardar el diagrama (opcional)"
                    }
                },
                "required": []
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
        
        elif name == "get_table_relationships":
            relationships = db_manager.get_table_relationships()
            
            if relationships:
                result_text = f"🔗 Relaciones entre tablas ({len(relationships)} encontradas):\n\n"
                for rel in relationships:
                    result_text += f"• {rel['parent_table']}.{rel['parent_column']} → {rel['child_table']}.{rel['child_column']}\n"
                    if rel['constraint_name']:
                        result_text += f"  Restricción: {rel['constraint_name']}\n"
                    result_text += f"  Actualización: {rel['update_rule']}, Eliminación: {rel['delete_rule']}\n\n"
            else:
                result_text = "🔗 No se encontraron relaciones entre tablas"
            
            return [types.TextContent(type="text", text=result_text)]
        
        elif name == "get_table_indexes":
            table_name = arguments["table_name"]
            indexes = db_manager.get_table_indexes(table_name)
            
            if indexes:
                result_text = f"📇 Índices de la tabla '{table_name}' ({len(indexes)} encontrados):\n\n"
                for idx in indexes:
                    unique_text = " (ÚNICO)" if idx["unique"] else ""
                    result_text += f"• {idx['index_name']}: {idx['column_name']}{unique_text}\n"
                    result_text += f"  Posición: {idx['ordinal_position']}, Tipo: {idx['type']}\n\n"
            else:
                result_text = f"📇 No se encontraron índices en la tabla '{table_name}'"
            
            return [types.TextContent(type="text", text=result_text)]
        
        elif name == "get_primary_keys":
            table_name = arguments["table_name"]
            primary_keys = db_manager.get_primary_keys(table_name)
            
            if primary_keys:
                result_text = f"🔑 Claves primarias de la tabla '{table_name}':\n\n"
                result_text += "\n".join([f"• {pk}" for pk in primary_keys])
            else:
                result_text = f"🔑 No se encontraron claves primarias en la tabla '{table_name}'"
            
            return [types.TextContent(type="text", text=result_text)]
        
        elif name == "generate_database_documentation":
            documentation = db_manager.generate_database_documentation()
            
            result_text = f"📚 Documentación de la base de datos generada:\n\n"
            result_text += f"📁 Archivo: {documentation['database_path']}\n"
            result_text += f"📊 Total de tablas: {documentation['summary']['total_tables']}\n"
            result_text += f"🔗 Total de relaciones: {documentation['summary']['total_relationships']}\n\n"
            
            result_text += "📋 Tablas:\n"
            for table_name, table_info in documentation["tables"].items():
                result_text += f"• {table_name} ({table_info['record_count']} registros)\n"
            
            return [types.TextContent(type="text", text=result_text)]
        
        elif name == "export_documentation_markdown":
            markdown_doc = db_manager.export_documentation_markdown()
            
            return [types.TextContent(
                type="text",
                text="📄 Documentación exportada en formato Markdown:\n\n" + markdown_doc
            )]
        
        elif name == "generate_enhanced_documentation":
            if not ENHANCED_DOC_AVAILABLE:
                return [types.TextContent(
                    type="text",
                    text="❌ Módulo de documentación mejorada no disponible. Instala las dependencias necesarias."
                )]
            
            include_er_diagram = arguments.get("include_er_diagram", True)
            include_data_quality = arguments.get("include_data_quality", True)
            include_field_analysis = arguments.get("include_field_analysis", True)
            
            try:
                enhanced_gen = EnhancedDocumentationGenerator(db_manager)
                documentation = enhanced_gen.generate_enhanced_documentation(
                    include_er_diagram=include_er_diagram,
                    include_data_quality=include_data_quality,
                    include_field_analysis=include_field_analysis
                )
                
                return [types.TextContent(
                    type="text",
                    text=f"📚 Documentación mejorada generada exitosamente:\n\n{documentation}"
                )]
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error generando documentación mejorada: {str(e)}"
                )]
        
        elif name == "export_documentation_html":
            if not ENHANCED_DOC_AVAILABLE:
                return [types.TextContent(
                    type="text",
                    text="❌ Módulo de documentación mejorada no disponible. Instala las dependencias necesarias."
                )]
            
            output_path = arguments.get("output_path")
            
            try:
                enhanced_gen = EnhancedDocumentationGenerator(db_manager)
                html_content = enhanced_gen.export_to_html()
                
                if output_path:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    return [types.TextContent(
                        type="text",
                        text=f"📄 Documentación HTML exportada a: {output_path}"
                    )]
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"📄 Documentación HTML generada:\n\n{html_content[:2000]}..."
                    )]
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error exportando HTML: {str(e)}"
                )]
        
        elif name == "export_documentation_json":
            if not ENHANCED_DOC_AVAILABLE:
                return [types.TextContent(
                    type="text",
                    text="❌ Módulo de documentación mejorada no disponible. Instala las dependencias necesarias."
                )]
            
            output_path = arguments.get("output_path")
            
            try:
                enhanced_gen = EnhancedDocumentationGenerator(db_manager)
                json_content = enhanced_gen.export_to_json()
                
                if output_path:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(json_content)
                    return [types.TextContent(
                        type="text",
                        text=f"📄 Documentación JSON exportada a: {output_path}"
                    )]
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"📄 Documentación JSON generada:\n\n{json_content[:2000]}..."
                    )]
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error exportando JSON: {str(e)}"
                )]
        
        elif name == "analyze_data_quality":
            if not ENHANCED_DOC_AVAILABLE:
                return [types.TextContent(
                    type="text",
                    text="❌ Módulo de documentación mejorada no disponible. Instala las dependencias necesarias."
                )]
            
            table_name = arguments.get("table_name")
            
            try:
                enhanced_gen = EnhancedDocumentationGenerator(db_manager)
                
                if table_name:
                    # Análisis de una tabla específica
                    analysis = enhanced_gen.analyze_data_quality_for_table(table_name)
                    result_text = f"📊 Análisis de calidad de datos para '{table_name}':\n\n"
                    result_text += f"• Total de registros: {analysis['total_records']}\n"
                    result_text += f"• Registros únicos: {analysis['unique_records']}\n"
                    result_text += f"• Registros duplicados: {analysis['duplicate_records']}\n"
                    result_text += f"• Campos con valores nulos: {analysis['null_fields']}\n"
                    result_text += f"• Campos con valores vacíos: {analysis['empty_fields']}\n"
                else:
                    # Análisis de todas las tablas
                    tables = db_manager.list_tables()
                    result_text = "📊 Análisis de calidad de datos (todas las tablas):\n\n"
                    
                    for table in tables:
                        analysis = enhanced_gen.analyze_data_quality_for_table(table)
                        result_text += f"📋 {table}:\n"
                        result_text += f"  • Registros: {analysis['total_records']}\n"
                        result_text += f"  • Únicos: {analysis['unique_records']}\n"
                        result_text += f"  • Duplicados: {analysis['duplicate_records']}\n"
                        result_text += f"  • Campos con nulos: {len(analysis['null_fields'])}\n\n"
                
                return [types.TextContent(type="text", text=result_text)]
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error analizando calidad de datos: {str(e)}"
                )]
        
        elif name == "generate_er_diagram":
            if not ENHANCED_DOC_AVAILABLE:
                return [types.TextContent(
                    type="text",
                    text="❌ Módulo de documentación mejorada no disponible. Instala las dependencias necesarias."
                )]
            
            output_path = arguments.get("output_path")
            
            try:
                enhanced_gen = EnhancedDocumentationGenerator(db_manager)
                mermaid_diagram = enhanced_gen.generate_er_diagram()
                
                if output_path:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(mermaid_diagram)
                    return [types.TextContent(
                        type="text",
                        text=f"📊 Diagrama ER exportado a: {output_path}\n\n{mermaid_diagram}"
                    )]
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"📊 Diagrama ER generado:\n\n{mermaid_diagram}"
                    )]
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error generando diagrama ER: {str(e)}"
                )]
        
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