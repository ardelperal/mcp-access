#!/usr/bin/env python3
"""
Test de Integración MCP Access Database
Verifica que el MCP esté correctamente integrado en otro proyecto
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path

def print_status(message, status="INFO"):
    """Imprime mensajes con formato"""
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️"
    }
    print(f"{icons.get(status, 'ℹ️')} {message}")

def test_mcp_integration():
    """Verifica que el MCP Access esté funcionando"""
    print_status("Iniciando test de integración MCP Access Database...")
    
    # Verificar estructura de directorios
    print_status("Verificando estructura de directorios...")
    
    required_paths = [
        "mcp-modules/mcp-access/src/mcp_access_server.py",
        "mcp-modules/mcp-access/requirements.txt",
        "mcp.json"
    ]
    
    for path in required_paths:
        if not os.path.exists(path):
            print_status(f"Archivo requerido no encontrado: {path}", "ERROR")
            return False
        else:
            print_status(f"Encontrado: {path}", "SUCCESS")
    
    # Verificar configuración MCP
    print_status("Verificando configuración MCP...")
    try:
        with open("mcp.json", "r") as f:
            config = json.load(f)
            
        if "mcpServers" in config and "mcp-access" in config["mcpServers"]:
            print_status("Configuración MCP válida", "SUCCESS")
        else:
            print_status("Configuración MCP inválida", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error leyendo configuración MCP: {e}", "ERROR")
        return False
    
    # Verificar dependencias
    print_status("Verificando dependencias...")
    try:
        import pyodbc
        print_status("pyodbc disponible", "SUCCESS")
    except ImportError:
        print_status("pyodbc no disponible - instalando...", "WARNING")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyodbc"])
    
    # Test básico del servidor MCP
    print_status("Probando servidor MCP...")
    try:
        # Cambiar al directorio del MCP
        mcp_dir = "mcp-modules/mcp-access"
        if os.path.exists(mcp_dir):
            # Ejecutar test rápido
            result = subprocess.run([
                sys.executable, 
                "tools/test_final_summary.py"
            ], cwd=mcp_dir, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print_status("Servidor MCP funcionando correctamente", "SUCCESS")
            else:
                print_status(f"Error en servidor MCP: {result.stderr}", "ERROR")
                return False
        else:
            print_status("Directorio MCP no encontrado", "ERROR")
            return False
            
    except subprocess.TimeoutExpired:
        print_status("Timeout en test del servidor MCP", "WARNING")
    except Exception as e:
        print_status(f"Error probando servidor MCP: {e}", "ERROR")
        return False
    
    print_status("✨ Integración MCP Access Database completada exitosamente!", "SUCCESS")
    return True

def show_usage_examples():
    """Muestra ejemplos de uso"""
    print("\n" + "="*60)
    print("📖 EJEMPLOS DE USO")
    print("="*60)
    
    print("""
1. Configuración básica en mcp.json:
{
  "mcpServers": {
    "mcp-access": {
      "command": "python",
      "args": ["mcp-modules/mcp-access/src/mcp_access_server.py"]
    }
  }
}

2. Uso en Trae AI:
   - El MCP estará disponible automáticamente
   - Puedes consultar bases de datos Access directamente
   - Ejemplo: "Muestra las tablas de la base de datos"

3. Comandos útiles:
   - Actualizar: git submodule update --remote mcp-modules/mcp-access
   - Diagnóstico: python mcp-modules/mcp-access/tools/test_final_summary.py
   - Configurar proxy: python mcp-modules/mcp-access/scripts/utils/detect_proxy.py
""")

def main():
    """Función principal"""
    print("🔗 Test de Integración - MCP Access Database")
    print("=" * 50)
    
    if test_mcp_integration():
        show_usage_examples()
        print("\n🎉 ¡Integración completada! El MCP Access Database está listo para usar.")
    else:
        print("\n💥 Error en la integración. Revisa los mensajes anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()