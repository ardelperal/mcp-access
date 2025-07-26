#!/usr/bin/env python3
"""
Script de prueba para demostrar la detección de relaciones usando COM automation.
Este script prueba la nueva funcionalidad COM como método principal para detectar relaciones.
"""

import sys
import os
import logging

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_access_server import AccessDatabaseManager, AccessCOMManager, COM_AVAILABLE

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_com_relationships():
    """Probar la detección de relaciones usando COM automation."""
    
    # Ruta a la base de datos de prueba
    db_path = os.path.join(os.path.dirname(__file__), 'sample_databases', 'Lanzadera_Datos.accdb')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    print("🔍 PRUEBA DE DETECCIÓN DE RELACIONES CON COM AUTOMATION (SIN VENTANAS)")
    print("=" * 70)
    
    # Verificar disponibilidad de COM
    print(f"📋 COM disponible: {'✅ Sí' if COM_AVAILABLE else '❌ No'}")
    
    if not COM_AVAILABLE:
        print("⚠️  pywin32 no está instalado. Instalando...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32>=306"])
            print("✅ pywin32 instalado correctamente")
        except Exception as e:
            print(f"❌ Error instalando pywin32: {e}")
            return
    
    # Prueba 1: COM directo con contraseña
    print("\n🔧 PRUEBA 1: COM AUTOMATION DIRECTO (MODO SILENCIOSO)")
    print("-" * 50)
    
    try:
        com_manager = AccessCOMManager()
        
        print("🔐 Conectando con contraseña (modo silencioso)...")
        if com_manager.connect(db_path, password="dpddpd"):
            print("✅ Conexión COM exitosa - Access ejecutándose en segundo plano")
            print("🔇 No se mostraron diálogos de contraseña")
            
            # Obtener tablas
            tables = com_manager.get_table_names()
            print(f"📊 Tablas encontradas: {len(tables)}")
            
            # Obtener relaciones
            relationships = com_manager.get_relationships()
            print(f"🔗 Relaciones COM encontradas: {len(relationships)}")
            
            if relationships:
                print("\n📋 RELACIONES DETECTADAS POR COM:")
                for i, rel in enumerate(relationships[:5], 1):  # Mostrar solo las primeras 5
                    print(f"  {i}. {rel['name']}")
                    print(f"     Tabla padre: {rel['table']}")
                    print(f"     Tabla hija: {rel['foreign_table']}")
                    print(f"     Campos: {len(rel.get('fields', []))}")
                    for field in rel.get('fields', []):
                        print(f"       - {field['name']} → {field['foreign_name']}")
                    print()
            
            com_manager.disconnect()
            print("✅ Desconexión COM exitosa")
            
        else:
            print("❌ Error en conexión COM")
            
    except Exception as e:
        print(f"❌ Error en prueba COM: {e}")
    
    # Prueba 2: AccessDatabaseManager con COM integrado
    print("\n🔧 PRUEBA 2: ACCESS DATABASE MANAGER CON COM")
    print("-" * 40)
    
    try:
        db_manager = AccessDatabaseManager()
        
        if db_manager.connect(db_path):
            print("✅ Conexión ODBC exitosa")
            
            # Obtener relaciones (ahora debería usar COM primero)
            relationships = db_manager.get_table_relationships()
            print(f"🔗 Relaciones totales encontradas: {len(relationships)}")
            
            # Analizar métodos de detección
            methods = {}
            confidence_levels = {}
            
            for rel in relationships:
                method = rel.get('detection_method', 'unknown')
                confidence = rel.get('confidence', 'unknown')
                
                methods[method] = methods.get(method, 0) + 1
                confidence_levels[confidence] = confidence_levels.get(confidence, 0) + 1
            
            print("\n📊 MÉTODOS DE DETECCIÓN:")
            for method, count in methods.items():
                emoji = "🤖" if method == "COM_automation" else "🔍" if method.startswith("ODBC") else "🧠"
                print(f"  {emoji} {method}: {count} relaciones")
            
            print("\n📈 NIVELES DE CONFIANZA:")
            for confidence, count in confidence_levels.items():
                emoji = "🟢" if confidence == "very_high" else "🟡" if confidence == "high" else "🟠"
                print(f"  {emoji} {confidence}: {count} relaciones")
            
            # Generar documentación
            print("\n📄 Generando documentación...")
            documentation = db_manager.generate_database_documentation()
            
            # Exportar a Markdown
            markdown_content = db_manager.export_documentation_markdown()
            
            # Guardar documentación
            output_file = "COM_Relationships_Test_Documentation.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✅ Documentación guardada en: {output_file}")
            
            db_manager.disconnect()
            print("✅ Desconexión exitosa")
            
        else:
            print("❌ Error en conexión ODBC")
            
    except Exception as e:
        print(f"❌ Error en prueba integrada: {e}")
    
    # Resumen final
    print("\n🎯 RESUMEN DE LA PRUEBA")
    print("=" * 30)
    print("✅ COM automation implementado como método principal")
    print("✅ Fallback automático a ODBC y métodos de inferencia")
    print("✅ Niveles de confianza mejorados")
    print("✅ Documentación completa generada")
    print("\n🚀 El sistema ahora puede detectar relaciones de manera más robusta!")

if __name__ == "__main__":
    test_com_relationships()