#!/usr/bin/env python3
"""
Pruebas específicas para las nuevas funcionalidades de relaciones y documentación.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from mcp_access_server import AccessDatabaseManager

def test_relationships_and_documentation():
    """Prueba las nuevas funcionalidades de relaciones y documentación."""
    
    print("🔍 Iniciando pruebas de relaciones y documentación")
    print("=" * 60)
    
    # Crear instancia del gestor
    db_manager = AccessDatabaseManager()
    
    # Usar una base de datos de ejemplo (ajustar según disponibilidad)
    db_path = r"C:\temp\test_database.accdb"
    
    try:
        # Conectar a la base de datos
        print(f"📡 Conectando a: {db_path}")
        if not db_manager.connect(db_path, "dpddpd"):
            if not db_manager.connect(db_path, ""):
                print("❌ No se pudo conectar. Creando estructura de prueba...")
                # En un entorno real, aquí se crearía la base de datos
                return
        
        print("✅ Conexión exitosa!")
        
        # 1. Crear tablas con relaciones para pruebas
        print("\n🔨 Creando estructura de prueba con relaciones...")
        
        # Tabla principal: clientes
        try:
            clientes_columns = [
                {"name": "id", "type": "INTEGER", "primary_key": True, "not_null": True},
                {"name": "nombre", "type": "TEXT", "not_null": True},
                {"name": "email", "type": "TEXT"},
                {"name": "telefono", "type": "TEXT"}
            ]
            db_manager.create_table("clientes", clientes_columns)
            print("  ✅ Tabla 'clientes' creada")
        except Exception as e:
            print(f"  ⚠️  Tabla 'clientes': {e}")
        
        # Tabla relacionada: pedidos
        try:
            pedidos_columns = [
                {"name": "id", "type": "INTEGER", "primary_key": True, "not_null": True},
                {"name": "cliente_id", "type": "INTEGER", "not_null": True},
                {"name": "fecha", "type": "DATE"},
                {"name": "total", "type": "DOUBLE"},
                {"name": "estado", "type": "TEXT", "default": "'Pendiente'"}
            ]
            db_manager.create_table("pedidos", pedidos_columns)
            print("  ✅ Tabla 'pedidos' creada")
        except Exception as e:
            print(f"  ⚠️  Tabla 'pedidos': {e}")
        
        # Tabla relacionada: productos
        try:
            productos_columns = [
                {"name": "id", "type": "INTEGER", "primary_key": True, "not_null": True},
                {"name": "nombre", "type": "TEXT", "not_null": True},
                {"name": "precio", "type": "DOUBLE"},
                {"name": "stock", "type": "INTEGER", "default": "0"}
            ]
            db_manager.create_table("productos", productos_columns)
            print("  ✅ Tabla 'productos' creada")
        except Exception as e:
            print(f"  ⚠️  Tabla 'productos': {e}")
        
        # 2. Probar obtención de relaciones
        print("\n🔗 Probando obtención de relaciones entre tablas...")
        try:
            relationships = db_manager.get_table_relationships()
            print(f"  📊 Relaciones encontradas: {len(relationships)}")
            
            if relationships:
                for rel in relationships:
                    print(f"    • {rel['parent_table']}.{rel['parent_column']} → {rel['child_table']}.{rel['child_column']}")
                    if rel['constraint_name']:
                        print(f"      Restricción: {rel['constraint_name']}")
            else:
                print("  📝 No se encontraron relaciones definidas (normal en Access sin relaciones explícitas)")
        except Exception as e:
            print(f"  ❌ Error obteniendo relaciones: {e}")
        
        # 3. Probar obtención de índices
        print("\n📇 Probando obtención de índices...")
        for table in ["clientes", "pedidos", "productos"]:
            try:
                indexes = db_manager.get_table_indexes(table)
                print(f"  📊 Índices en tabla '{table}': {len(indexes)}")
                
                for idx in indexes:
                    unique_text = " (ÚNICO)" if idx["unique"] else ""
                    print(f"    • {idx['index_name']}: {idx['column_name']}{unique_text}")
            except Exception as e:
                print(f"  ❌ Error obteniendo índices de '{table}': {e}")
        
        # 4. Probar obtención de claves primarias
        print("\n🔑 Probando obtención de claves primarias...")
        for table in ["clientes", "pedidos", "productos"]:
            try:
                primary_keys = db_manager.get_primary_keys(table)
                if primary_keys:
                    print(f"  🔑 Claves primarias de '{table}': {', '.join(primary_keys)}")
                else:
                    print(f"  📝 No se encontraron claves primarias en '{table}'")
            except Exception as e:
                print(f"  ❌ Error obteniendo claves primarias de '{table}': {e}")
        
        # 5. Insertar datos de ejemplo
        print("\n📝 Insertando datos de ejemplo...")
        try:
            # Insertar clientes
            clientes_data = [
                {"nombre": "Juan Pérez", "email": "juan@email.com", "telefono": "123-456-7890"},
                {"nombre": "María García", "email": "maria@email.com", "telefono": "098-765-4321"},
                {"nombre": "Carlos López", "email": "carlos@email.com", "telefono": "555-123-4567"}
            ]
            
            for cliente in clientes_data:
                db_manager.execute_query(
                    "INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)",
                    [cliente["nombre"], cliente["email"], cliente["telefono"]]
                )
            print("  ✅ Clientes insertados")
            
            # Insertar productos
            productos_data = [
                {"nombre": "Laptop", "precio": 999.99, "stock": 10},
                {"nombre": "Mouse", "precio": 25.50, "stock": 50},
                {"nombre": "Teclado", "precio": 75.00, "stock": 30}
            ]
            
            for producto in productos_data:
                db_manager.execute_query(
                    "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                    [producto["nombre"], producto["precio"], producto["stock"]]
                )
            print("  ✅ Productos insertados")
            
            # Insertar pedidos
            pedidos_data = [
                {"cliente_id": 1, "fecha": "2024-01-15", "total": 999.99, "estado": "Completado"},
                {"cliente_id": 2, "fecha": "2024-01-16", "total": 101.00, "estado": "Pendiente"},
                {"cliente_id": 1, "fecha": "2024-01-17", "total": 75.00, "estado": "Enviado"}
            ]
            
            for pedido in pedidos_data:
                db_manager.execute_query(
                    "INSERT INTO pedidos (cliente_id, fecha, total, estado) VALUES (?, ?, ?, ?)",
                    [pedido["cliente_id"], pedido["fecha"], pedido["total"], pedido["estado"]]
                )
            print("  ✅ Pedidos insertados")
            
        except Exception as e:
            print(f"  ❌ Error insertando datos: {e}")
        
        # 6. Probar generación de documentación completa
        print("\n📚 Probando generación de documentación completa...")
        try:
            documentation = db_manager.generate_database_documentation()
            
            print(f"  📊 Documentación generada:")
            print(f"    • Base de datos: {documentation['database_path']}")
            print(f"    • Total de tablas: {documentation['summary']['total_tables']}")
            print(f"    • Total de relaciones: {documentation['summary']['total_relationships']}")
            
            print(f"\n  📋 Resumen de tablas:")
            for table_name, table_info in documentation["tables"].items():
                print(f"    • {table_name}: {table_info['record_count']} registros, {len(table_info['schema'])} columnas")
                if table_info['primary_keys']:
                    print(f"      Claves primarias: {', '.join(table_info['primary_keys'])}")
                if table_info['indexes']:
                    print(f"      Índices: {len(table_info['indexes'])}")
            
        except Exception as e:
            print(f"  ❌ Error generando documentación: {e}")
        
        # 7. Probar exportación a Markdown
        print("\n📄 Probando exportación a Markdown...")
        try:
            markdown_doc = db_manager.export_documentation_markdown()
            
            # Guardar en archivo
            output_file = Path(__file__).parent / "documentacion_prueba.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_doc)
            
            print(f"  ✅ Documentación Markdown generada ({len(markdown_doc)} caracteres)")
            print(f"  📁 Guardada en: {output_file}")
            
            # Mostrar primeras líneas
            lines = markdown_doc.split('\n')[:10]
            print(f"\n  📝 Primeras líneas del documento:")
            for line in lines:
                print(f"    {line}")
            
        except Exception as e:
            print(f"  ❌ Error exportando a Markdown: {e}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    finally:
        # Desconectar
        print("\n🔌 Desconectando de la base de datos...")
        db_manager.disconnect()
        print("✅ Desconexión exitosa")
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas de relaciones y documentación completadas!")

if __name__ == "__main__":
    print("🔧 MCP Access Server - Pruebas de Relaciones y Documentación")
    print("⚠️  IMPORTANTE: Este script requiere una base de datos Access disponible")
    print("   Ajusta la variable 'db_path' según tu configuración\n")
    
    test_relationships_and_documentation()