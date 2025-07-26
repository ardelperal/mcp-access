#!/usr/bin/env python3
"""
test_pip_install.py - Script para probar que pip install funciona correctamente
"""

import subprocess
import sys
import os
from pathlib import Path

def test_pip_connectivity():
    """Probar conectividad de pip"""
    print("🧪 PRUEBA: Verificando funcionamiento de pip install")
    print("=" * 60)
    
    # Verificar configuración actual de pip
    print("📋 Verificando configuración actual de pip...")
    
    # Mostrar configuración de pip
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "config", "list"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Configuración de pip:")
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    print(f"   {line}")
            else:
                print("   (Sin configuración personalizada)")
        else:
            print("⚠️ No se pudo obtener la configuración de pip")
    except Exception as e:
        print(f"⚠️ Error obteniendo configuración: {e}")
    
    print("\n🌐 Probando conectividad con PyPI...")
    
    # Probar con un paquete muy pequeño y común
    test_packages = [
        "six",  # Paquete muy pequeño y estable
        "certifi",  # Certificados SSL
        "urllib3"  # Librería de HTTP
    ]
    
    for package in test_packages:
        print(f"\n📦 Probando instalación de '{package}'...")
        try:
            # Usar --dry-run para no instalar realmente, solo verificar conectividad
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "--dry-run", "--quiet", package
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ {package}: Conectividad OK")
                return True
            else:
                print(f"   ❌ {package}: Error - {result.stderr.strip()}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ {package}: Timeout - posible problema de conectividad")
        except Exception as e:
            print(f"   ❌ {package}: Error inesperado - {e}")
    
    print("\n🔄 Probando instalación real de un paquete pequeño...")
    try:
        # Probar instalación real de certifi (muy pequeño y útil)
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", "certifi"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("   ✅ Instalación real exitosa!")
            print("   📋 Salida:")
            for line in result.stdout.strip().split('\n')[-5:]:  # Últimas 5 líneas
                if line.strip():
                    print(f"      {line}")
            return True
        else:
            print("   ❌ Error en instalación real:")
            print(f"      {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ⏱️ Timeout en instalación real")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

def test_proxy_detection():
    """Probar detección de proxy"""
    print("\n🔍 Verificando detección automática de proxy...")
    
    try:
        # Ejecutar nuestro detector de proxy
        result = subprocess.run([sys.executable, "detect_proxy.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Detector de proxy ejecutado correctamente")
            # Mostrar solo las líneas importantes
            lines = result.stdout.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['detectó', 'configuración', 'proxy', 'Ivanti', '✅', '❌']):
                    print(f"   {line}")
        else:
            print("⚠️ Error ejecutando detector de proxy")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")

def main():
    """Función principal"""
    print("🧪 PRUEBA COMPLETA: pip install y configuración de proxy")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not Path("detect_proxy.py").exists():
        print("❌ Error: No se encuentra detect_proxy.py en el directorio actual")
        print("   Asegúrese de ejecutar desde el directorio mcp-access")
        return
    
    # Probar detección de proxy
    test_proxy_detection()
    
    # Probar pip install
    success = test_pip_connectivity()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 RESULTADO: pip install funciona correctamente!")
        print("   ✅ La configuración de proxy es correcta")
        print("   ✅ Conectividad con PyPI establecida")
        print("   ✅ Listo para instalar dependencias del proyecto")
    else:
        print("❌ RESULTADO: Hay problemas con pip install")
        print("   🔧 Revisar configuración de proxy")
        print("   🌐 Verificar conectividad a internet")
        print("   📞 Contactar administrador de red si es necesario")
    
    print("\nPresione Enter para continuar...")
    input()

if __name__ == "__main__":
    main()