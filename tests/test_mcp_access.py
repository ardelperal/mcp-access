#!/usr/bin/env python3
"""
Pruebas unitarias para el MCP Access Server.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import AccessMCPConfig, AccessDataTypes, QueryBuilder, AccessUtils

class TestAccessMCPConfig(unittest.TestCase):
    """Pruebas para la configuración del MCP."""
    
    def test_get_config(self):
        """Probar obtención de configuración."""
        config = AccessMCPConfig.get_config()
        self.assertIsInstance(config, dict)
        self.assertIn("server", config)
        self.assertIn("database", config)
        self.assertIn("logging", config)
        self.assertIn("security", config)
    
    def test_connection_string_accdb(self):
        """Probar generación de cadena de conexión para .accdb."""
        conn_str = AccessMCPConfig.get_connection_string("test.accdb")
        self.assertIn("Microsoft Access Driver (*.mdb, *.accdb)", conn_str)
        self.assertIn("DBQ=test.accdb", conn_str)
    
    def test_connection_string_mdb(self):
        """Probar generación de cadena de conexión para .mdb."""
        conn_str = AccessMCPConfig.get_connection_string("test.mdb")
        self.assertIn("Microsoft Access Driver (*.mdb)", conn_str)
        self.assertIn("DBQ=test.mdb", conn_str)

class TestAccessDataTypes(unittest.TestCase):
    """Pruebas para tipos de datos de Access."""
    
    def test_get_type_info(self):
        """Probar obtención de información de tipos."""
        info = AccessDataTypes.get_type_info("TEXT")
        self.assertIn("Texto corto", info)
        
        info = AccessDataTypes.get_type_info("UNKNOWN")
        self.assertEqual(info, "Tipo desconocido")
    
    def test_list_types(self):
        """Probar listado de tipos."""
        types = AccessDataTypes.list_types()
        self.assertIsInstance(types, dict)
        self.assertIn("TEXT", types)
        self.assertIn("INTEGER", types)
        self.assertIn("DOUBLE", types)

class TestQueryBuilder(unittest.TestCase):
    """Pruebas para el constructor de consultas."""
    
    def test_select_basic(self):
        """Probar SELECT básico."""
        query = QueryBuilder.select("empleados")
        self.assertEqual(query, "SELECT * FROM empleados")
    
    def test_select_with_columns(self):
        """Probar SELECT con columnas específicas."""
        query = QueryBuilder.select("empleados", ["nombre", "apellido"])
        self.assertEqual(query, "SELECT nombre, apellido FROM empleados")
    
    def test_select_with_where(self):
        """Probar SELECT con WHERE."""
        query = QueryBuilder.select("empleados", where="salario > 50000")
        self.assertEqual(query, "SELECT * FROM empleados WHERE salario > 50000")
    
    def test_select_with_order_by(self):
        """Probar SELECT con ORDER BY."""
        query = QueryBuilder.select("empleados", order_by="nombre ASC")
        self.assertEqual(query, "SELECT * FROM empleados ORDER BY nombre ASC")
    
    def test_select_with_limit(self):
        """Probar SELECT con LIMIT (TOP en Access)."""
        query = QueryBuilder.select("empleados", limit=10)
        self.assertEqual(query, "SELECT TOP 10 * FROM empleados")
    
    def test_select_complete(self):
        """Probar SELECT completo con todas las opciones."""
        query = QueryBuilder.select(
            "empleados", 
            ["nombre", "salario"], 
            "departamento = 'IT'", 
            "salario DESC", 
            5
        )
        expected = "SELECT TOP 5 nombre, salario FROM empleados WHERE departamento = 'IT' ORDER BY salario DESC"
        self.assertEqual(query, expected)
    
    def test_insert(self):
        """Probar construcción de INSERT."""
        data = {"nombre": "Juan", "apellido": "Pérez", "salario": 50000}
        query, values = QueryBuilder.insert("empleados", data)
        
        expected_query = "INSERT INTO empleados (nombre, apellido, salario) VALUES (?, ?, ?)"
        expected_values = ["Juan", "Pérez", 50000]
        
        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)
    
    def test_update(self):
        """Probar construcción de UPDATE."""
        data = {"salario": 55000, "departamento": "IT"}
        query, values = QueryBuilder.update("empleados", data, "id = 1")
        
        expected_query = "UPDATE empleados SET salario = ?, departamento = ? WHERE id = 1"
        expected_values = [55000, "IT"]
        
        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)
    
    def test_delete(self):
        """Probar construcción de DELETE."""
        query = QueryBuilder.delete("empleados", "id = 1")
        expected = "DELETE FROM empleados WHERE id = 1"
        self.assertEqual(query, expected)
    
    def test_create_table_basic(self):
        """Probar construcción de CREATE TABLE básico."""
        columns = [
            {"name": "id", "type": "INTEGER"},
            {"name": "nombre", "type": "TEXT"}
        ]
        query = QueryBuilder.create_table("test_table", columns)
        expected = "CREATE TABLE test_table (id INTEGER, nombre TEXT)"
        self.assertEqual(query, expected)
    
    def test_create_table_with_constraints(self):
        """Probar CREATE TABLE con restricciones."""
        columns = [
            {
                "name": "id", 
                "type": "INTEGER", 
                "primary_key": True, 
                "not_null": True,
                "auto_increment": True
            },
            {
                "name": "nombre", 
                "type": "TEXT", 
                "not_null": True
            },
            {
                "name": "activo", 
                "type": "YESNO", 
                "default": "True"
            }
        ]
        query = QueryBuilder.create_table("test_table", columns)
        
        self.assertIn("id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT", query)
        self.assertIn("nombre TEXT NOT NULL", query)
        self.assertIn("activo YESNO DEFAULT True", query)

class TestAccessUtils(unittest.TestCase):
    """Pruebas para utilidades de Access."""
    
    def test_validate_database_path_valid_accdb(self):
        """Probar validación de ruta válida .accdb."""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".accdb", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            self.assertTrue(AccessUtils.validate_database_path(tmp_path))
        finally:
            os.unlink(tmp_path)
    
    def test_validate_database_path_valid_mdb(self):
        """Probar validación de ruta válida .mdb."""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".mdb", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            self.assertTrue(AccessUtils.validate_database_path(tmp_path))
        finally:
            os.unlink(tmp_path)
    
    def test_validate_database_path_invalid_extension(self):
        """Probar validación con extensión inválida."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            self.assertFalse(AccessUtils.validate_database_path(tmp_path))
        finally:
            os.unlink(tmp_path)
    
    def test_validate_database_path_nonexistent(self):
        """Probar validación con archivo inexistente."""
        self.assertFalse(AccessUtils.validate_database_path("nonexistent.accdb"))
    
    def test_validate_database_path_empty(self):
        """Probar validación con ruta vacía."""
        self.assertFalse(AccessUtils.validate_database_path(""))
        self.assertFalse(AccessUtils.validate_database_path(None))
    
    def test_format_results_table_empty(self):
        """Probar formateo de tabla vacía."""
        result = AccessUtils.format_results_table([])
        self.assertEqual(result, "No hay resultados")
    
    def test_format_results_table_with_data(self):
        """Probar formateo de tabla con datos."""
        results = [
            {"id": 1, "nombre": "Juan", "salario": 50000},
            {"id": 2, "nombre": "María", "salario": 55000}
        ]
        
        result = AccessUtils.format_results_table(results)
        
        # Verificar que contiene los encabezados
        self.assertIn("id", result)
        self.assertIn("nombre", result)
        self.assertIn("salario", result)
        
        # Verificar que contiene los datos
        self.assertIn("Juan", result)
        self.assertIn("María", result)
        self.assertIn("50000", result)
        self.assertIn("55000", result)
        
        # Verificar que tiene separadores
        self.assertIn("|", result)
        self.assertIn("-", result)
    
    def test_format_results_table_with_nulls(self):
        """Probar formateo con valores NULL."""
        results = [
            {"id": 1, "nombre": "Juan", "email": None},
            {"id": 2, "nombre": "María", "email": "maria@test.com"}
        ]
        
        result = AccessUtils.format_results_table(results)
        self.assertIn("NULL", result)
        self.assertIn("maria@test.com", result)
    
    def test_escape_sql_identifier(self):
        """Probar escape de identificadores SQL."""
        escaped = AccessUtils.escape_sql_identifier("tabla con espacios")
        self.assertEqual(escaped, "[tabla con espacios]")
        
        escaped = AccessUtils.escape_sql_identifier("tabla_normal")
        self.assertEqual(escaped, "[tabla_normal]")
    
    def test_get_sample_queries(self):
        """Probar obtención de consultas de ejemplo."""
        queries = AccessUtils.get_sample_queries()
        self.assertIsInstance(queries, dict)
        self.assertIn("listar_tablas", queries)
        self.assertIn("contar_registros", queries)
        self.assertIn("estructura_tabla", queries)

class TestAccessDatabaseManagerMock(unittest.TestCase):
    """Pruebas para AccessDatabaseManager usando mocks."""
    
    def setUp(self):
        """Configurar pruebas."""
        # Importar aquí para evitar problemas si pyodbc no está disponible
        try:
            from mcp_access_server import AccessDatabaseManager
            self.AccessDatabaseManager = AccessDatabaseManager
        except ImportError:
            self.skipTest("pyodbc no disponible")
    
    @patch('mcp_access_server.pyodbc.connect')
    @patch('mcp_access_server.Path')
    def test_connect_success(self, mock_path, mock_connect):
        """Probar conexión exitosa."""
        # Configurar mocks
        mock_path.return_value.exists.return_value = True
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        # Crear instancia y conectar
        db_manager = self.AccessDatabaseManager()
        result = db_manager.connect("test.accdb")
        
        # Verificar
        self.assertTrue(result)
        self.assertEqual(db_manager.connection, mock_connection)
        self.assertEqual(db_manager.database_path, "test.accdb")
    
    @patch('mcp_access_server.Path')
    def test_connect_file_not_found(self, mock_path):
        """Probar conexión con archivo inexistente."""
        # Configurar mock
        mock_path.return_value.exists.return_value = False
        
        # Crear instancia y conectar
        db_manager = self.AccessDatabaseManager()
        result = db_manager.connect("nonexistent.accdb")
        
        # Verificar
        self.assertFalse(result)
        self.assertIsNone(db_manager.connection)
    
    def test_disconnect(self):
        """Probar desconexión."""
        db_manager = self.AccessDatabaseManager()
        
        # Simular conexión activa
        mock_connection = Mock()
        db_manager.connection = mock_connection
        db_manager.database_path = "test.accdb"
        
        # Desconectar
        db_manager.disconnect()
        
        # Verificar
        mock_connection.close.assert_called_once()
        self.assertIsNone(db_manager.connection)
        self.assertIsNone(db_manager.database_path)
    
    def test_is_connected(self):
        """Probar verificación de conexión."""
        db_manager = self.AccessDatabaseManager()
        
        # Sin conexión
        self.assertFalse(db_manager.is_connected())
        
        # Con conexión
        db_manager.connection = Mock()
        self.assertTrue(db_manager.is_connected())

def run_tests():
    """Ejecutar todas las pruebas."""
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar clases de prueba
    test_classes = [
        TestAccessMCPConfig,
        TestAccessDataTypes,
        TestQueryBuilder,
        TestAccessUtils,
        TestAccessDatabaseManagerMock
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print(f"RESUMEN DE PRUEBAS")
    print(f"{'='*50}")
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Omitidas: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.errors:
        print(f"\nERRORES:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    if result.failures:
        print(f"\nFALLOS:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    # Retornar True si todas las pruebas pasaron
    return len(result.errors) == 0 and len(result.failures) == 0

if __name__ == "__main__":
    print("🧪 Ejecutando pruebas unitarias del MCP Access Server")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n✅ ¡Todas las pruebas pasaron exitosamente!")
        sys.exit(0)
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        sys.exit(1)