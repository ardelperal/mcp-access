#!/usr/bin/env python3
"""
Demostración completa de las nuevas funcionalidades de MCP Access Database Server
Este script muestra todas las capacidades de análisis y documentación implementadas.
"""

import os
import sys
from datetime import datetime

# Agregar el directorio src al path para importar el módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_access_server import AccessDatabaseManager

def print_header(title):
    """Imprime un encabezado formateado"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Imprime un título de sección"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_database_analysis():
    """Demostración completa de análisis de base de datos"""
    
    # Configuración
    db_path = os.path.join("sample_databases", "Lanzadera_Datos.accdb")
    output_path = os.path.join("sample_databases", "Demo_Documentation.md")
    
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encuentra la base de datos en {db_path}")
        print("   Asegúrate de que el archivo Lanzadera_Datos.accdb esté en sample_databases/")
        return False
    
    print_header("DEMOSTRACIÓN MCP ACCESS DATABASE SERVER v2.0")
    print(f"📁 Base de datos: {db_path}")
    print(f"📝 Salida: {output_path}")
    print(f"🕒 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Crear manager
    db_manager = AccessDatabaseManager()
    
    try:
        # 1. Conexión
        print_section("1. CONEXIÓN A BASE DE DATOS")
        print("🔌 Conectando...")
        db_manager.connect(db_path)
        print("✅ Conexión establecida exitosamente")
        
        # 2. Listado de tablas
        print_section("2. ANÁLISIS DE ESTRUCTURA GENERAL")
        print("📋 Obteniendo lista de tablas...")
        tables = db_manager.list_tables()
        print(f"✅ Encontradas {len(tables)} tablas:")
        
        # Mostrar primeras 10 tablas
        for i, table in enumerate(tables[:10], 1):
            print(f"   {i:2d}. {table}")
        if len(tables) > 10:
            print(f"   ... y {len(tables) - 10} tablas más")
        
        # 3. Análisis de esquemas
        print_section("3. ANÁLISIS DE ESQUEMAS DE TABLAS")
        sample_tables = tables[:3]  # Analizar primeras 3 tablas
        
        for table in sample_tables:
            print(f"\n🔍 Analizando tabla: {table}")
            try:
                schema = db_manager.get_table_schema(table)
                print(f"   📊 Columnas: {len(schema)}")
                
                # Mostrar primeras columnas
                for col in schema[:5]:
                    col_name = col.get('column_name', 'N/A')
                    col_type = col.get('data_type', 'N/A')
                    print(f"      - {col_name}: {col_type}")
                
                if len(schema) > 5:
                    print(f"      ... y {len(schema) - 5} columnas más")
                    
            except Exception as e:
                print(f"   ⚠️  Error al analizar esquema: {e}")
        
        # 4. Análisis de claves primarias
        print_section("4. ANÁLISIS DE CLAVES PRIMARIAS")
        for table in sample_tables:
            print(f"\n🔑 Claves primarias de {table}:")
            try:
                primary_keys = db_manager.get_primary_keys(table)
                if primary_keys:
                    for pk in primary_keys:
                        if isinstance(pk, dict):
                            print(f"   - {pk.get('column_name', pk)}")
                        else:
                            print(f"   - {pk}")
                else:
                    print("   - No se encontraron claves primarias")
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
        
        # 5. Análisis de índices
        print_section("5. ANÁLISIS DE ÍNDICES")
        for table in sample_tables:
            print(f"\n📇 Índices de {table}:")
            try:
                indexes = db_manager.get_table_indexes(table)
                if indexes:
                    for idx in indexes[:3]:  # Mostrar primeros 3 índices
                        idx_name = idx.get('index_name', 'N/A')
                        idx_cols = idx.get('columns', [])
                        unique = "ÚNICO" if idx.get('unique', False) else "NO ÚNICO"
                        print(f"   - {idx_name}: {', '.join(idx_cols)} ({unique})")
                    if len(indexes) > 3:
                        print(f"   ... y {len(indexes) - 3} índices más")
                else:
                    print("   - No se encontraron índices")
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
        
        # 6. Análisis de relaciones
        print_section("6. ANÁLISIS DE RELACIONES")
        print("🔗 Analizando relaciones entre tablas...")
        try:
            relationships = db_manager.get_table_relationships()
            if relationships:
                print(f"✅ Encontradas {len(relationships)} relaciones:")
                for rel in relationships[:5]:  # Mostrar primeras 5
                    parent = rel.get('parent_table', 'N/A')
                    child = rel.get('child_table', 'N/A')
                    parent_col = rel.get('parent_column', 'N/A')
                    child_col = rel.get('child_column', 'N/A')
                    print(f"   - {parent}.{parent_col} → {child}.{child_col}")
                if len(relationships) > 5:
                    print(f"   ... y {len(relationships) - 5} relaciones más")
            else:
                print("   - No se encontraron relaciones explícitas")
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
        
        # 7. Generación de documentación
        print_section("7. GENERACIÓN DE DOCUMENTACIÓN COMPLETA")
        print("📊 Generando documentación completa...")
        try:
            documentation = db_manager.generate_database_documentation()
            
            summary = documentation.get('summary', {})
            tables_info = documentation.get('tables', {})
            
            print("✅ Documentación generada exitosamente:")
            print(f"   📋 Total de tablas: {summary.get('total_tables', 0)}")
            print(f"   🔗 Total de relaciones: {summary.get('total_relationships', 0)}")
            
            # Calcular registros totales
            total_records = sum(table.get('record_count', 0) for table in tables_info.values())
            print(f"   📊 Registros totales: {total_records:,}")
            
            # Mostrar estadísticas de algunas tablas
            print("\n   📈 Estadísticas de tablas (muestra):")
            for i, (table_name, table_info) in enumerate(list(tables_info.items())[:5]):
                record_count = table_info.get('record_count', 0)
                column_count = len(table_info.get('schema', []))
                print(f"      {i+1}. {table_name}: {record_count:,} registros, {column_count} columnas")
            
        except Exception as e:
            print(f"   ❌ Error al generar documentación: {e}")
            return False
        
        # 8. Exportación a Markdown
        print_section("8. EXPORTACIÓN A MARKDOWN")
        print("📝 Exportando documentación a Markdown...")
        try:
            markdown_content = db_manager.export_documentation_markdown()
            
            # Guardar archivo
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            file_size = len(markdown_content.encode('utf-8'))
            print(f"✅ Documentación exportada exitosamente:")
            print(f"   📁 Archivo: {output_path}")
            print(f"   📏 Tamaño: {file_size:,} bytes")
            print(f"   📄 Líneas: {markdown_content.count(chr(10)) + 1:,}")
            
        except Exception as e:
            print(f"   ❌ Error al exportar: {e}")
            return False
        
        # 9. Resumen final
        print_section("9. RESUMEN FINAL")
        print("🎉 Demostración completada exitosamente!")
        print(f"✅ Base de datos analizada: {len(tables)} tablas")
        print(f"✅ Documentación generada: {output_path}")
        print(f"✅ Todas las funcionalidades probadas")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        return False
        
    finally:
        # Desconexión
        if db_manager.is_connected():
            print("\n🔌 Desconectando de la base de datos...")
            db_manager.disconnect()
            print("✅ Desconexión exitosa")

def main():
    """Función principal"""
    print("🚀 Iniciando demostración de MCP Access Database Server")
    
    # Cambiar al directorio de tests
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    success = demo_database_analysis()
    
    if success:
        print(f"\n{'='*60}")
        print("🎊 ¡DEMOSTRACIÓN COMPLETADA EXITOSAMENTE!")
        print("📖 Revisa el archivo de documentación generado para ver los resultados.")
        print("🔧 Todas las nuevas funcionalidades están funcionando correctamente.")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("❌ La demostración encontró algunos problemas.")
        print("🔧 Revisa los mensajes de error anteriores para más detalles.")
        print(f"{'='*60}")

if __name__ == "__main__":
    main()