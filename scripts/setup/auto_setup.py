#!/usr/bin/env python3
"""
auto_setup.py - Configuración automática multiplataforma para MCP Access Database
"""

import os
import sys
import json
import platform
import subprocess
import shutil
import winreg
from pathlib import Path

class MCPSetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.home = Path.home()
        self.setup_paths()
        
    def setup_paths(self):
        """Configurar rutas según el sistema operativo"""
        if self.system == "windows":
            self.mcp_dir = self.home / ".mcp" / "servers" / "mcp-access"
            self.config_file = self.home / ".mcp" / "config.json"
            self.python_cmd = "python"
        else:  # Linux/macOS
            self.mcp_dir = self.home / ".mcp" / "servers" / "mcp-access"
            self.config_file = self.home / ".mcp" / "config.json"
            self.python_cmd = "python3"
    
    def check_ivanti_connection(self):
        """Verificar si Ivanti VPN está activo"""
        if self.system != "windows":
            return False
            
        self.log("Verificando Ivanti VPN...")
        
        try:
            # Verificar procesos de Ivanti
            result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq ivanti*"], 
                                  capture_output=True, text=True)
            if "ivanti" in result.stdout.lower():
                self.log("🏢 Ivanti VPN detectado (proceso activo)")
                return True
            
            # Verificar servicios de Ivanti
            result = subprocess.run(["sc", "query", "type=service", "state=running"], 
                                  capture_output=True, text=True)
            if "ivanti" in result.stdout.lower():
                self.log("🏢 Ivanti VPN detectado (servicio activo)")
                return True
            
            # Verificar adaptadores de red VPN
            result = subprocess.run(["ipconfig", "/all"], 
                                  capture_output=True, text=True)
            if any(keyword in result.stdout.lower() for keyword in ["ivanti", "pulse", "vpn"]):
                self.log("🏢 Conexión VPN detectada")
                return True
            
            # Verificar rutas de red que indiquen VPN corporativa
            result = subprocess.run(["route", "print"], 
                                  capture_output=True, text=True)
            # Buscar rutas típicas de redes corporativas
            corporate_networks = ["10.0.0.0", "172.16.0.0", "192.168.0.0"]
            for network in corporate_networks:
                if network in result.stdout:
                    self.log("🏢 Red corporativa detectada")
                    return True
            
            return False
            
        except Exception as e:
            self.log(f"⚠️ Error verificando Ivanti: {e}", "WARNING")
            return False
    
    def detect_proxy(self):
        """Detectar configuración de proxy automáticamente"""
        proxy_config = {}
        
        if self.system == "windows":
            # Verificar si Ivanti está activo
            ivanti_detected = self.check_ivanti_connection()
            
            try:
                # Verificar proxy en WinHTTP
                result = subprocess.run(["netsh", "winhttp", "show", "proxy"], 
                                      capture_output=True, text=True)
                if "servidor proxy" in result.stdout.lower() and "directo" not in result.stdout.lower():
                    # Extraer proxy de WinHTTP
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "servidor proxy" in line.lower():
                            proxy_line = line.split(':')
                            if len(proxy_line) > 1:
                                proxy_config['http_proxy'] = f"http://{proxy_line[1].strip()}"
                                proxy_config['https_proxy'] = f"http://{proxy_line[1].strip()}"
                
                # Verificar proxy en Internet Settings si no se encontró en WinHTTP
                if not proxy_config:
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
                    except (FileNotFoundError, OSError):
                        pass
                
                # Si Ivanti está activo pero no se detectó proxy, usar proxy corporativo
                if ivanti_detected and not proxy_config:
                    self.log("🏢 Ivanti VPN detectado - aplicando configuración de proxy corporativo")
                    proxy_config['http_proxy'] = "http://185.46.212.88:80"
                    proxy_config['https_proxy'] = "http://185.46.212.88:80"
                        
            except Exception as e:
                self.log(f"⚠️ No se pudo detectar proxy: {e}", "WARNING")
        
        else:  # Linux/macOS
            # Verificar variables de entorno
            for var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
                value = os.environ.get(var)
                if value:
                    proxy_config[var.lower()] = value
        
        if proxy_config:
            self.log(f"🌐 Proxy detectado: {proxy_config}")
            return proxy_config
        else:
            self.log("🌐 No se detectó configuración de proxy")
            return None
    
    def configure_proxy_for_tools(self, proxy_config):
        """Configurar proxy para herramientas (git, pip)"""
        if not proxy_config:
            return
            
        self.log("Configurando proxy para herramientas...")
        
        # Configurar Git
        if 'http_proxy' in proxy_config:
            try:
                subprocess.run(["git", "config", "--global", "http.proxy", proxy_config['http_proxy']], 
                             check=True)
                subprocess.run(["git", "config", "--global", "https.proxy", proxy_config.get('https_proxy', proxy_config['http_proxy'])], 
                             check=True)
                self.log("✅ Git configurado con proxy")
            except Exception as e:
                self.log(f"⚠️ Error configurando Git con proxy: {e}", "WARNING")
        
        # Configurar pip
        if self.system == "windows":
            pip_dir = self.home / "AppData" / "Roaming" / "pip"
            pip_dir.mkdir(parents=True, exist_ok=True)
            pip_config = pip_dir / "pip.ini"
            
            config_content = "[global]\n"
            if 'http_proxy' in proxy_config:
                config_content += f"proxy = {proxy_config['http_proxy']}\n"
            
            with open(pip_config, 'w') as f:
                f.write(config_content)
            self.log("✅ pip configurado con proxy")
        else:
            # Para Linux/macOS, usar variables de entorno
            for key, value in proxy_config.items():
                os.environ[key] = value
            self.log("✅ Variables de entorno de proxy configuradas")
    
    def log(self, message, level="INFO"):
        """Logging con colores"""
        colors = {
            "INFO": "\033[0;32m",
            "WARNING": "\033[1;33m", 
            "ERROR": "\033[0;31m",
            "RESET": "\033[0m"
        }
        
        if self.system == "windows":
            print(f"[{level}] {message}")
        else:
            color = colors.get(level, colors["RESET"])
            print(f"{color}[{level}] {message}{colors['RESET']}")
    
    def check_dependencies(self):
        """Verificar dependencias del sistema"""
        self.log("Verificando dependencias...")
        
        # Verificar Python
        try:
            result = subprocess.run([self.python_cmd, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ Python encontrado: {result.stdout.strip()}")
            else:
                raise Exception("Python no funciona correctamente")
        except Exception as e:
            self.log(f"❌ Python no encontrado: {e}", "ERROR")
            return False
        
        # Verificar Git
        try:
            result = subprocess.run(["git", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ Git encontrado: {result.stdout.strip()}")
            else:
                raise Exception("Git no funciona correctamente")
        except Exception as e:
            self.log(f"❌ Git no encontrado: {e}", "ERROR")
            return False
        
        return True
    
    def create_directories(self):
        """Crear directorios necesarios"""
        self.log("Creando directorios...")
        self.mcp_dir.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.log("✅ Directorios creados")
    
    def sync_repository(self, repo_url):
        """Sincronizar repositorio"""
        self.log("Sincronizando repositorio...")
        
        if (self.mcp_dir / ".git").exists():
            self.log("Actualizando repositorio existente...")
            os.chdir(self.mcp_dir)
            subprocess.run(["git", "fetch", "origin"], check=True)
            subprocess.run(["git", "reset", "--hard", "origin/main"], check=True)
        else:
            self.log("Clonando repositorio...")
            if self.mcp_dir.exists():
                shutil.rmtree(self.mcp_dir)
            subprocess.run(["git", "clone", repo_url, str(self.mcp_dir)], check=True)
        
        self.log("✅ Repositorio sincronizado")
    
    def install_dependencies(self):
        """Instalar dependencias de Python"""
        self.log("Instalando dependencias...")
        os.chdir(self.mcp_dir)
        
        pip_cmd = "pip" if self.system == "windows" else "pip3"
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        
        self.log("✅ Dependencias instaladas")
    
    def configure_mcp(self):
        """Configurar MCP"""
        self.log("Configurando MCP...")
        
        # Crear configuración base si no existe
        if not self.config_file.exists():
            config = {"mcpServers": {}}
        else:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        
        # Configuración del MCP Access
        mcp_config = {
            "access-db": {
                "command": self.python_cmd,
                "args": [str(self.mcp_dir / "src" / "mcp_access_server.py")],
                "env": {
                    "PYTHONPATH": str(self.mcp_dir / "src"),
                    "MCP_ACCESS_LOG_LEVEL": "INFO"
                },
                "description": "Microsoft Access Database MCP Server"
            }
        }
        
        # Fusionar configuraciones
        config["mcpServers"].update(mcp_config)
        
        # Guardar configuración
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.log("✅ MCP configurado")
    
    def verify_installation(self):
        """Verificar instalación"""
        self.log("Verificando instalación...")
        
        try:
            os.chdir(self.mcp_dir)
            result = subprocess.run([
                self.python_cmd, 
                "src/mcp_access_server.py", 
                "--version"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ MCP verificado correctamente")
                return True
            else:
                self.log("⚠️ No se pudo verificar el MCP", "WARNING")
                return False
        except Exception as e:
            self.log(f"⚠️ Error en verificación: {e}", "WARNING")
            return False
    
    def setup(self, repo_url):
        """Proceso completo de configuración"""
        try:
            self.log("🚀 Iniciando configuración automática...")
            
            if not self.check_dependencies():
                return False
            
            # Detectar y configurar proxy automáticamente
            proxy_config = self.detect_proxy()
            self.configure_proxy_for_tools(proxy_config)
            
            self.create_directories()
            self.sync_repository(repo_url)
            self.install_dependencies()
            self.configure_mcp()
            
            # Detectar proxy usando el script utilitario
            detect_proxy_path = os.path.join(self.mcp_dir, 'utils', 'detect_proxy.py')
            if os.path.exists(detect_proxy_path):
                try:
                    result = subprocess.run([sys.executable, detect_proxy_path], 
                                          capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        self.log("✓ Detección de proxy completada")
                        if "Proxy configurado" in result.stdout:
                            self.log("✓ Proxy detectado y configurado automáticamente")
                        else:
                            self.log("ℹ No se detectó configuración de proxy")
                    else:
                        self.log(f"⚠ Advertencia en detección de proxy: {result.stderr}", "WARNING")
                except Exception as e:
                    self.log(f"⚠ Error en detección de proxy: {e}", "WARNING")
            else:
                self.log("⚠ Script de detección de proxy no encontrado", "WARNING")
            
            self.verify_installation()
            
            self.log("🎉 Configuración completada!")
            self.log(f"MCP instalado en: {self.mcp_dir}")
            self.log(f"Configuración en: {self.config_file}")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error durante la configuración: {e}", "ERROR")
            return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python auto_setup.py <URL_DEL_REPOSITORIO>")
        print("Ejemplo: python auto_setup.py https://github.com/usuario/mcp-access-database.git")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    setup = MCPSetup()
    
    success = setup.setup(repo_url)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()