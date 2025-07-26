#!/usr/bin/env python3
"""
Script de prueba para demostrar las nuevas capacidades de detección de relaciones
del MCP Access Database Server.
"""

import sys
import os
import json

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_access_server import AccessDatabaseManager

def test_relationship_detection():
    """Probar todas las capacidades de detección de relaciones."""
    
    # Ruta a la base de datos de prueba
    db_path = os.path.join(os.path.dirname(__file__), 'sample_databases', 'Lanzadera_Datos.accdb')
    
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos en {db_path}")
        return
    
    print("🔍 PRUEBA DE DETECCIÓN DE RELACIONES")
    print("=" * 50)
    
    # Crear instancia del gestor
    db_manager = AccessDatabaseManager()
    
    try:
        # Conectar a la base de datos
        print(f"📂 Conectando a: {db_path}")
        success = db_manager.connect(db_path)
        if success:
            print(f"✅ Conexión exitosa")
        else:
            print(f"❌ Error al conectar")
            return
        
        # Obtener lista de tablas
        print("\n📋 Obteniendo lista de tablas...")
        tables = db_manager.list_tables()
        print(f"✅ Encontradas {len(tables)} tablas")
        
        # Probar detección de relaciones
        print("\n🔗 DETECTANDO RELACIONES...")
        print("-" * 30)
        
        relationships = db_manager.get_table_relationships()
        
        if relationships:
            print(f"✅ Se detectaron {len(relationships)} relaciones:")
            
            # Agrupar por método de detección
            methods = {}
            confidence_levels = {}
            
            for rel in relationships:
                method = rel.get('detection_method', 'unknown')
                confidence = rel.get('confidence', 'unknown')
                
                if method not in methods:
                    methods[method] = []
                methods[method].append(rel)
                
                if confidence != 'unknown':
                    confidence_levels[confidence] = confidence_levels.get(confidence, 0) + 1
            
            # Mostrar estadísticas
            print(f"\n📊 ESTADÍSTICAS DE DETECCIÓN:")
            for method, rels in methods.items():
                method_names = {
                    "ODBC_foreignKeys": "🔗 ODBC Foreign Keys",
                    "MSysRelationships": "🏛️ Tablas del Sistema Access",
                    "column_name_inference": "🔤 Inferencia por Nombres",
                    "data_pattern_analysis": "📊 Análisis de Patrones",
                    "index_analysis": "📇 Análisis de Índices"
                }
                method_display = method_names.get(method, f"❓ {method}")
                print(f"  {method_display}: {len(rels)} relaciones")
            
            if confidence_levels:
                print(f"\n🎯 NIVELES DE CONFIANZA:")
                for confidence, count in confidence_levels.items():
                    emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(confidence, "⚪")
                    print(f"  {emoji} {confidence.title()}: {count} relaciones")
            
            # Mostrar relaciones detalladas
            print(f"\n📝 RELACIONES DETECTADAS:")
            for i, rel in enumerate(relationships, 1):
                method_emoji = {
                    "ODBC_foreignKeys": "🔗",
                    "MSysRelationships": "🏛️",
                    "column_name_inference": "🔤",
                    "data_pattern_analysis": "📊",
                    "index_analysis": "📇"
                }.get(rel.get('detection_method', ''), "❓")
                
                confidence_emoji = {
                    "high": "🟢",
                    "medium": "🟡",
                    "low": "🔴"
                }.get(rel.get('confidence', ''), "")
                
                print(f"\n{i}. {method_emoji} {rel['parent_table']}.{rel['parent_column']} → {rel['child_table']}.{rel['child_column']} {confidence_emoji}")
                print(f"   Restricción: {rel['constraint_name']}")
                print(f"   Método: {rel.get('detection_method', 'unknown')}")
                if rel.get('confidence'):
                    print(f"   Confianza: {rel['confidence']}")
        else:
            print("⚠️ No se detectaron relaciones")
        
        # Generar documentación completa
        print(f"\n📚 GENERANDO DOCUMENTACIÓN COMPLETA...")
        documentation = db_manager.generate_database_documentation()
        
        # Exportar a Markdown
        print(f"📄 Exportando documentación a Markdown...")
        markdown_content = db_manager.export_documentation_markdown()
        
        # Guardar archivo
        output_file = os.path.join(os.path.dirname(__file__), 'sample_databases', 'Relationships_Test_Documentation.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Documentación guardada en: {output_file}")
        
        # Mostrar resumen final
        print(f"\n🎉 RESUMEN FINAL:")
        print(f"  📊 Tablas analizadas: {len(tables)}")
        print(f"  🔗 Relaciones detectadas: {len(relationships)}")
        if documentation.get('summary', {}).get('relationship_detection_methods'):
            print(f"  🔧 Métodos utilizados: {len(documentation['summary']['relationship_detection_methods'])}")
        
        # Análisis de tablas con más relaciones
        if relationships:
            table_counts = {}
            for rel in relationships:
                parent = rel['parent_table']
                child = rel['child_table']
                table_counts[parent] = table_counts.get(parent, 0) + 1
                table_counts[child] = table_counts.get(child, 0) + 1
            
            if table_counts:
                most_connected = max(table_counts.items(), key=lambda x: x[1])
                print(f"  🏆 Tabla más conectada: {most_connected[0]} ({most_connected[1]} relaciones)")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Desconectar
        try:
            db_manager.disconnect()
            print(f"\n🔌 Desconectado de la base de datos")
        except:
            pass

if __name__ == "__main__":
    test_relationship_detection()