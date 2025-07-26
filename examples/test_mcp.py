#!/usr/bin/env python3
"""
Script de ejemplo para probar el servidor MCP de Access.
Este script demuestra cómo usar todas las funcionalidades del MCP.
"""

import asyncio
import json
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / "src"))

from mcp_access_server import AccessDatabaseManager

async def test_access_operations():
    """Función de prueba para demostrar las operaciones del MCP."""
    
    print("🚀 Iniciando pruebas del MCP Access Server")
    print("=" * 50)
    
    # Crear instancia del gestor
    db_manager = AccessDatabaseManager()
    
    # Ruta de ejemplo (ajusta según tu base de datos)
    db_path = r"C:\ruta\a\tu\base_de_datos.accdb"
    
    try:
        # 1. Conectar a la base de datos
        print(f"📡 Conectando a: {db_path}")
        # Probar primero con contraseña por defecto
        if not db_manager.connect(db_path, "dpddpd"):
            print("❌ No se pudo conectar con contraseña por defecto. Probando sin contraseña...")
            if not db_manager.connect(db_path, ""):
                print("❌ No se pudo conectar. Creando base de datos de ejemplo...")
                # En un entorno real, aquí crearías la base de datos
                return
        
        print("✅ Conexión exitosa!")
        
        # 2. Listar tablas existentes
        print("\n📋 Listando tablas existentes:")
        tables = db_manager.list_tables()
        for table in tables:
            print(f"  • {table}")
        
        # 3. Crear una tabla de ejemplo
        print("\n🔨 Creando tabla de ejemplo 'empleados':")
        columns = [
            {"name": "id", "type": "INTEGER", "primary_key": True, "not_null": True},
            {"name": "nombre", "type": "TEXT", "not_null": True},
            {"name": "apellido", "type": "TEXT", "not_null": True},
            {"name": "email", "type": "TEXT"},
            {"name": "salario", "type": "DOUBLE"},
            {"name": "fecha_ingreso", "type": "DATE"}
        ]
        
        try:
            db_manager.create_table("empleados", columns)
            print("✅ Tabla 'empleados' creada exitosamente")
        except Exception as e:
            print(f"⚠️  La tabla ya existe o error: {e}")
        
        # 4. Obtener esquema de la tabla
        print("\n📊 Esquema de la tabla 'empleados':")
        try:
            schema = db_manager.get_table_schema("empleados")
            for col in schema:
                nullable = "NULL" if col["nullable"] else "NOT NULL"
                print(f"  • {col['column_name']} - {col['data_type']} {nullable}")
        except Exception as e:
            print(f"❌ Error obteniendo esquema: {e}")
        
        # 5. Insertar datos de ejemplo
        print("\n📝 Insertando datos de ejemplo:")
        sample_data = [
            {
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@empresa.com",
                "salario": 50000.00,
                "fecha_ingreso": "2023-01-15"
            },
            {
                "nombre": "María",
                "apellido": "García",
                "email": "maria.garcia@empresa.com",
                "salario": 55000.00,
                "fecha_ingreso": "2023-02-20"
            },
            {
                "nombre": "Carlos",
                "apellido": "López",
                "email": "carlos.lopez@empresa.com",
                "salario": 48000.00,
                "fecha_ingreso": "2023-03-10"
            }
        ]
        
        for i, data in enumerate(sample_data, 1):
            try:
                # Simular inserción (en el MCP real usarías la herramienta insert_record)
                columns = list(data.keys())
                values = list(data.values())
                placeholders = ", ".join(["?" for _ in values])
                query = f"INSERT INTO empleados ({', '.join(columns)}) VALUES ({placeholders})"
                db_manager.execute_query(query, values)
                print(f"  ✅ Empleado {i} insertado")
            except Exception as e:
                print(f"  ⚠️  Error insertando empleado {i}: {e}")
        
        # 6. Consultar datos
        print("\n🔍 Consultando todos los empleados:")
        try:
            results = db_manager.execute_query("SELECT * FROM empleados")
            if results:
                print(f"  📊 Encontrados {len(results)} empleados:")
                for emp in results:
                    print(f"    • {emp.get('nombre', 'N/A')} {emp.get('apellido', 'N/A')} - ${emp.get('salario', 0):,.2f}")
            else:
                print("  📊 No se encontraron empleados")
        except Exception as e:
            print(f"  ❌ Error consultando empleados: {e}")
        
        # 7. Actualizar un registro
        print("\n✏️  Actualizando salario de Juan Pérez:")
        try:
            result = db_manager.execute_query(
                "UPDATE empleados SET salario = ? WHERE nombre = ? AND apellido = ?",
                [52000.00, "Juan", "Pérez"]
            )
            affected = result[0]["affected_rows"] if result else 0
            print(f"  ✅ Registros actualizados: {affected}")
        except Exception as e:
            print(f"  ❌ Error actualizando: {e}")
        
        # 8. Consulta con filtros
        print("\n🔍 Consultando empleados con salario > $50,000:")
        try:
            results = db_manager.execute_query(
                "SELECT nombre, apellido, salario FROM empleados WHERE salario > ?",
                [50000]
            )
            if results:
                for emp in results:
                    print(f"  • {emp['nombre']} {emp['apellido']} - ${emp['salario']:,.2f}")
            else:
                print("  📊 No se encontraron empleados con ese criterio")
        except Exception as e:
            print(f"  ❌ Error en consulta filtrada: {e}")
        
        # 9. Eliminar un registro
        print("\n🗑️  Eliminando empleado Carlos López:")
        try:
            result = db_manager.execute_query(
                "DELETE FROM empleados WHERE nombre = ? AND apellido = ?",
                ["Carlos", "López"]
            )
            affected = result[0]["affected_rows"] if result else 0
            print(f"  ✅ Registros eliminados: {affected}")
        except Exception as e:
            print(f"  ❌ Error eliminando: {e}")
        
        # 10. Consulta final
        print("\n📊 Estado final de la tabla empleados:")
        try:
            results = db_manager.execute_query("SELECT COUNT(*) as total FROM empleados")
            if results:
                total = results[0]["total"]
                print(f"  📈 Total de empleados: {total}")
        except Exception as e:
            print(f"  ❌ Error contando empleados: {e}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    finally:
        # Desconectar
        print("\n🔌 Desconectando de la base de datos...")
        db_manager.disconnect()
        print("✅ Desconexión exitosa")
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")

def print_mcp_usage_examples():
    """Imprimir ejemplos de uso del MCP."""
    
    print("\n" + "=" * 60)
    print("📚 EJEMPLOS DE USO DEL MCP ACCESS SERVER")
    print("=" * 60)
    
    examples = [
        {
            "title": "1. Conectar a una base de datos sin contraseña",
            "tool": "connect_database",
            "args": {
                "database_path": "C:\\ruta\\a\\mi_base_datos.accdb"
            }
        },
        {
            "title": "1b. Conectar a una base de datos con contraseña",
            "tool": "connect_database",
            "args": {
                "database_path": "C:\\ruta\\a\\mi_base_datos.accdb",
                "password": "mi_contraseña_secreta"
            }
        },
        {
            "title": "1c. Conectar usando contraseña por defecto",
            "tool": "connect_database",
            "args": {
                "database_path": "C:\\ruta\\a\\mi_base_datos.accdb",
                "password": "dpddpd"
            }
        },
        {
            "title": "2. Listar todas las tablas",
            "tool": "list_tables",
            "args": {}
        },
        {
            "title": "3. Obtener esquema de una tabla",
            "tool": "get_table_schema",
            "args": {
                "table_name": "empleados"
            }
        },
        {
            "title": "4. Crear una nueva tabla",
            "tool": "create_table",
            "args": {
                "table_name": "productos",
                "columns": [
                    {"name": "id", "type": "INTEGER", "primary_key": True},
                    {"name": "nombre", "type": "TEXT", "not_null": True},
                    {"name": "precio", "type": "DOUBLE"},
                    {"name": "stock", "type": "INTEGER", "default": "0"}
                ]
            }
        },
        {
            "title": "5. Insertar un registro",
            "tool": "insert_record",
            "args": {
                "table_name": "empleados",
                "data": {
                    "nombre": "Ana",
                    "apellido": "Martínez",
                    "email": "ana.martinez@empresa.com",
                    "salario": 60000
                }
            }
        },
        {
            "title": "6. Actualizar registros",
            "tool": "update_record",
            "args": {
                "table_name": "empleados",
                "data": {"salario": 65000},
                "where_clause": "nombre = 'Ana' AND apellido = 'Martínez'"
            }
        },
        {
            "title": "7. Obtener registros con filtros",
            "tool": "get_records",
            "args": {
                "table_name": "empleados",
                "columns": ["nombre", "apellido", "salario"],
                "where_clause": "salario > 50000",
                "order_by": "salario DESC",
                "limit": 10
            }
        },
        {
            "title": "8. Ejecutar consulta SQL personalizada",
            "tool": "execute_query",
            "args": {
                "query": "SELECT AVG(salario) as salario_promedio FROM empleados"
            }
        },
        {
            "title": "9. Eliminar registros",
            "tool": "delete_record",
            "args": {
                "table_name": "empleados",
                "where_clause": "fecha_ingreso < '2023-01-01'"
            }
        },
        {
            "title": "10. Eliminar una tabla",
            "tool": "drop_table",
            "args": {
                "table_name": "tabla_temporal"
            }
        }
    ]
    
    for example in examples:
        print(f"\n{example['title']}:")
        print(f"Herramienta: {example['tool']}")
        print(f"Argumentos: {json.dumps(example['args'], indent=2, ensure_ascii=False)}")
        print("-" * 40)

if __name__ == "__main__":
    print("🔧 MCP Access Server - Script de Pruebas y Ejemplos")
    
    # Mostrar ejemplos de uso
    print_mcp_usage_examples()
    
    # Preguntar si ejecutar pruebas
    print("\n¿Deseas ejecutar las pruebas con una base de datos real? (y/n): ", end="")
    response = input().lower().strip()
    
    if response in ['y', 'yes', 's', 'si', 'sí']:
        print("\n⚠️  IMPORTANTE: Asegúrate de tener:")
        print("  1. Microsoft Access Database Engine instalado")
        print("  2. Una base de datos Access (.accdb o .mdb) disponible")
        print("  3. Permisos de escritura en la base de datos")
        
        print("\nIngresa la ruta completa a tu base de datos Access: ", end="")
        db_path = input().strip()
        
        if db_path and Path(db_path).exists():
            # Ejecutar pruebas
            asyncio.run(test_access_operations())
        else:
            print("❌ La ruta especificada no existe o está vacía")
    else:
        print("\n✅ Ejemplos mostrados. Para usar el MCP, configúralo en tu cliente MCP compatible.")