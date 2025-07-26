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
            
            self.create_directories()
            self.sync_repository(repo_url)
            self.install_dependencies()
            self.configure_mcp()
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