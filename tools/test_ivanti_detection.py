#!/usr/bin/env python3
"""
test_ivanti_detection.py - Script de prueba para simular detección de Ivanti
"""

import os
import sys
import platform
import subprocess
import winreg
from pathlib import Path

def simulate_ivanti_detection():
    """Simular detección de Ivanti para pruebas"""
    print("🧪 MODO PRUEBA: Simulando Ivanti VPN activo")
    return True

def detect_windows_proxy_test():
    """Detectar configuración de proxy en Windows (modo prueba)"""
    proxy_config = {}
    
    print("🔍 Detectando configuración de proxy...")
    
    # Simular Ivanti activo
    ivanti_detected = simulate_ivanti_detection()
    
    try:
        # Verificar proxy en WinHTTP
        print("   Verificando WinHTTP...")
        result = subprocess.run(["netsh", "winhttp", "show", "proxy"], 
                              capture_output=True, text=True)
        
        if "servidor proxy" in result.stdout.lower() and "directo" not in result.stdout.lower():
            # Extraer proxy de WinHTTP
            lines = result.stdout.split('\n')
            for line in lines:
                if "servidor proxy" in line.lower():
                    proxy_line = line.split(':')
                    if len(proxy_line) > 1:
                        proxy_url = proxy_line[1].strip()
                        if not proxy_url.startswith("http"):
                            proxy_url = f"http://{proxy_url}"
                        proxy_config['http_proxy'] = proxy_url
                        proxy_config['https_proxy'] = proxy_url
                        print(f"   ✅ Proxy WinHTTP encontrado: {proxy_url}")
        
        # Verificar proxy en Internet Settings si no se encontró en WinHTTP
        if not proxy_config:
            print("   Verificando Internet Settings...")
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                  r"Software\Microsoft\Windows\CurrentVersion\Internet Settings") as key:
                    proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
                    if proxy_enable:
                        proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
                        if proxy_server:
                            if "://" not in proxy_server:
                                proxy_server = f"http://{proxy_server}"
                            proxy_config['http_proxy'] = proxy_server
                            proxy_config['https_proxy'] = proxy_server
                            print(f"   ✅ Proxy IE encontrado: {proxy_server}")
            except (FileNotFoundError, OSError):
                print("   ⚠️ No se pudo acceder a Internet Settings")
        
        # Si Ivanti está activo pero no se detectó proxy, usar proxy común de oficina
        if ivanti_detected and not proxy_config:
            print("   🏢 Ivanti detectado - aplicando configuración de proxy corporativo")
            # Proxy común usado en oficinas con Ivanti
            proxy_config['http_proxy'] = "http://185.46.212.88:80"
            proxy_config['https_proxy'] = "http://185.46.212.88:80"
            print(f"   ✅ Proxy corporativo aplicado: {proxy_config['http_proxy']}")
                
    except Exception as e:
        print(f"   ❌ Error detectando proxy: {e}")
    
    return proxy_config

def main():
    """Función principal de prueba"""
    print("🧪 PRUEBA: Detector de proxy con Ivanti simulado")
    print("=" * 60)
    
    if platform.system().lower() != "windows":
        print("❌ Este script está diseñado para Windows")
        sys.exit(1)
    
    # Detectar proxy con Ivanti simulado
    proxy_config = detect_windows_proxy_test()
    
    if proxy_config:
        print(f"\n✅ Proxy detectado:")
        for key, value in proxy_config.items():
            print(f"   {key}: {value}")
        
        print(f"\n🎯 RESULTADO: Con Ivanti activo, se aplicaría automáticamente:")
        print(f"   - Git proxy: {proxy_config.get('http_proxy', 'N/A')}")
        print(f"   - pip proxy: {proxy_config.get('http_proxy', 'N/A')}")
        print(f"   - Configuración automática: ✅ SÍ")
    else:
        print("\n❌ No se detectó configuración de proxy")
    
    print("\n" + "=" * 60)
    print("Presione Enter para continuar...")
    input()

if __name__ == "__main__":
    main()