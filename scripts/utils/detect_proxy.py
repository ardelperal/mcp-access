#!/usr/bin/env python3
"""
detect_proxy.py - Detección automática de configuración de proxy en Windows
"""

import os
import sys
import platform
import subprocess
import winreg
from pathlib import Path

def check_ivanti_connection():
    """Verificar si Ivanti VPN está activo"""
    print("   Verificando Ivanti VPN...")
    
    try:
        # Verificar procesos de Ivanti
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq ivanti*"], 
                              capture_output=True, text=True)
        if "ivanti" in result.stdout.lower():
            print("   🏢 Ivanti VPN detectado (proceso activo)")
            return True
        
        # Verificar servicios de Ivanti
        result = subprocess.run(["sc", "query", "type=service", "state=running"], 
                              capture_output=True, text=True)
        if "ivanti" in result.stdout.lower():
            print("   🏢 Ivanti VPN detectado (servicio activo)")
            return True
        
        # Verificar adaptadores de red VPN
        result = subprocess.run(["ipconfig", "/all"], 
                              capture_output=True, text=True)
        if any(keyword in result.stdout.lower() for keyword in ["ivanti", "pulse", "vpn"]):
            print("   🏢 Conexión VPN detectada")
            return True
        
        # Verificar rutas de red que indiquen VPN corporativa
        result = subprocess.run(["route", "print"], 
                              capture_output=True, text=True)
        # Buscar rutas típicas de redes corporativas
        corporate_networks = ["10.0.0.0", "172.16.0.0", "192.168.0.0"]
        for network in corporate_networks:
            if network in result.stdout:
                print("   🏢 Red corporativa detectada")
                return True
        
        print("   ℹ️ No se detectó Ivanti VPN")
        return False
        
    except Exception as e:
        print(f"   ⚠️ Error verificando Ivanti: {e}")
        return False

def detect_windows_proxy():
    """Detectar configuración de proxy en Windows"""
    proxy_config = {}
    
    print("🔍 Detectando configuración de proxy...")
    
    # Verificar si Ivanti está activo
    ivanti_detected = check_ivanti_connection()
    
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

def configure_git_proxy(proxy_config):
    """Configurar Git con proxy"""
    if not proxy_config:
        return False
        
    print("🔧 Configurando Git con proxy...")
    
    try:
        if 'http_proxy' in proxy_config:
            subprocess.run(["git", "config", "--global", "http.proxy", proxy_config['http_proxy']], 
                         check=True)
            subprocess.run(["git", "config", "--global", "https.proxy", proxy_config.get('https_proxy', proxy_config['http_proxy'])], 
                         check=True)
            print("   ✅ Git configurado con proxy")
            return True
    except Exception as e:
        print(f"   ❌ Error configurando Git: {e}")
        return False

def configure_pip_proxy(proxy_config):
    """Configurar pip con proxy"""
    if not proxy_config:
        return False
        
    print("🔧 Configurando pip con proxy...")
    
    try:
        home = Path.home()
        pip_dir = home / "AppData" / "Roaming" / "pip"
        pip_dir.mkdir(parents=True, exist_ok=True)
        pip_config = pip_dir / "pip.ini"
        
        config_content = "[global]\n"
        if 'http_proxy' in proxy_config:
            config_content += f"proxy = {proxy_config['http_proxy']}\n"
        
        with open(pip_config, 'w') as f:
            f.write(config_content)
        print("   ✅ pip configurado con proxy")
        return True
    except Exception as e:
        print(f"   ❌ Error configurando pip: {e}")
        return False

def main():
    """Función principal"""
    print("🌐 Detector automático de proxy para Windows")
    print("=" * 50)
    
    if platform.system().lower() != "windows":
        print("❌ Este script está diseñado para Windows")
        sys.exit(1)
    
    # Detectar proxy
    proxy_config = detect_windows_proxy()
    
    if proxy_config:
        print(f"\n✅ Proxy detectado:")
        for key, value in proxy_config.items():
            print(f"   {key}: {value}")
        
        # Preguntar si configurar herramientas
        print("\n¿Desea configurar Git y pip con este proxy? (s/n): ", end="")
        response = input().lower().strip()
        
        if response in ['s', 'si', 'y', 'yes']:
            configure_git_proxy(proxy_config)
            configure_pip_proxy(proxy_config)
            print("\n🎉 Configuración completada!")
        else:
            print("\n⏭️ Configuración omitida")
    else:
        print("\n🌐 No se detectó configuración de proxy")
        print("   El sistema parece usar conexión directa a internet")
    
    print("\n" + "=" * 50)
    print("Presione Enter para continuar...")
    input()

if __name__ == "__main__":
    main()