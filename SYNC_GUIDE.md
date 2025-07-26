# 🔄 Guía de Sincronización Multi-Máquina

## 📋 Estrategias de Sincronización

### 🥇 **Opción 1: GitHub Repository (Recomendada)**

#### **Configuración Inicial:**

1. **Crear repositorio en GitHub:**
   ```bash
   # En tu máquina principal
   cd C:\Users\adm1\Desktop\Proyectos\mcp-access
   git init
   git add .
   git commit -m "Initial MCP Access Database commit"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/mcp-access-database.git
   git push -u origin main
   ```

2. **En cada máquina nueva:**
   ```bash
   # Windows
   sync_mcp.bat
   
   # Linux/macOS
   chmod +x sync_mcp.sh
   ./sync_mcp.sh
   
   # Multiplataforma (Python)
   python auto_setup.py https://github.com/TU_USUARIO/mcp-access-database.git
   ```

#### **Actualización Regular:**
```bash
# Ejecutar en cualquier máquina para sincronizar
git pull origin main
pip install -r requirements.txt  # Si hay nuevas dependencias
```

---

### 🥈 **Opción 2: Cloud Storage (Dropbox/OneDrive/Google Drive)**

#### **Configuración:**

1. **Mover MCP a carpeta sincronizada:**
   ```bash
   # Windows
   move "C:\Users\adm1\.mcp\servers\mcp-access" "C:\Users\adm1\Dropbox\MCPs\mcp-access"
   mklink /D "C:\Users\adm1\.mcp\servers\mcp-access" "C:\Users\adm1\Dropbox\MCPs\mcp-access"
   ```

2. **Actualizar configuración:**
   ```json
   {
     "mcpServers": {
       "access-db": {
         "command": "python",
         "args": ["C:\\Users\\adm1\\Dropbox\\MCPs\\mcp-access\\src\\mcp_access_server.py"],
         "env": {
           "PYTHONPATH": "C:\\Users\\adm1\\Dropbox\\MCPs\\mcp-access\\src"
         }
       }
     }
   }
   ```

---

### 🥉 **Opción 3: Script de Sincronización Personalizado**

#### **Configuración con rsync (Linux/macOS):**
```bash
#!/bin/bash
# sync_to_server.sh
rsync -avz --delete ~/.mcp/servers/mcp-access/ user@servidor:/shared/mcp-access/
ssh user@servidor "cd /shared/mcp-access && pip install -r requirements.txt"
```

#### **Configuración con robocopy (Windows):**
```batch
@echo off
robocopy "C:\Users\%USERNAME%\.mcp\servers\mcp-access" "\\servidor\shared\mcp-access" /MIR /Z /W:1 /R:1
```

---

## 🚀 **Scripts de Automatización Incluidos**

### **1. `sync_mcp.bat` (Windows)**
- ✅ Clona/actualiza desde GitHub
- ✅ Instala dependencias automáticamente
- ✅ Configura MCP en Trae
- ✅ Verifica instalación

### **2. `sync_mcp.sh` (Linux/macOS)**
- ✅ Compatible con sistemas Unix
- ✅ Manejo de errores robusto
- ✅ Logging con colores
- ✅ Configuración automática con jq

### **3. `auto_setup.py` (Multiplataforma)**
- ✅ Funciona en Windows, Linux y macOS
- ✅ Detección automática del sistema
- ✅ Manejo inteligente de rutas
- ✅ Verificación completa

---

## 📱 **Configuración por Plataforma**

### **Windows:**
```batch
# Descarga e instala
curl -O https://raw.githubusercontent.com/TU_USUARIO/mcp-access-database/main/sync_mcp.bat
sync_mcp.bat

# O con Python
python -c "import urllib.request; urllib.request.urlretrieve('https://raw.githubusercontent.com/TU_USUARIO/mcp-access-database/main/auto_setup.py', 'auto_setup.py')"
python auto_setup.py https://github.com/TU_USUARIO/mcp-access-database.git
```

### **Linux/Ubuntu:**
```bash
# Descarga e instala
wget https://raw.githubusercontent.com/TU_USUARIO/mcp-access-database/main/sync_mcp.sh
chmod +x sync_mcp.sh
./sync_mcp.sh

# O con Python
python3 -c "import urllib.request; urllib.request.urlretrieve('https://raw.githubusercontent.com/TU_USUARIO/mcp-access-database/main/auto_setup.py', 'auto_setup.py')"
python3 auto_setup.py https://github.com/TU_USUARIO/mcp-access-database.git
```

### **macOS:**
```bash
# Con Homebrew
brew install git python3

# Descarga e instala
curl -O https://raw.githubusercontent.com/TU_USUARIO/mcp-access-database/main/sync_mcp.sh
chmod +x sync_mcp.sh
./sync_mcp.sh
```

---

## 🔧 **Configuración Avanzada**

### **Variables de Entorno Globales:**
```bash
# .bashrc / .zshrc (Linux/macOS)
export MCP_ACCESS_REPO="https://github.com/TU_USUARIO/mcp-access-database.git"
export MCP_ACCESS_DIR="$HOME/.mcp/servers/mcp-access"

# PowerShell Profile (Windows)
$env:MCP_ACCESS_REPO = "https://github.com/TU_USUARIO/mcp-access-database.git"
$env:MCP_ACCESS_DIR = "$env:USERPROFILE\.mcp\servers\mcp-access"
```

### **Cron Job para Actualización Automática (Linux/macOS):**
```bash
# Agregar a crontab -e
0 9 * * * cd ~/.mcp/servers/mcp-access && git pull origin main && pip3 install -r requirements.txt
```

### **Tarea Programada (Windows):**
```batch
schtasks /create /tn "MCP Access Sync" /tr "C:\Users\%USERNAME%\.mcp\servers\mcp-access\sync_mcp.bat" /sc daily /st 09:00
```

---

## 🔍 **Verificación y Troubleshooting**

### **Verificar Estado:**
```bash
# Verificar instalación
python ~/.mcp/servers/mcp-access/src/mcp_access_server.py --version

# Verificar configuración
cat ~/.mcp/config.json | grep -A 10 "access-db"

# Verificar logs de Trae
tail -f ~/AppData/Roaming/Trae/logs/*/window1/exthost/mcp-servers-host.log
```

### **Problemas Comunes:**

1. **Error de permisos:**
   ```bash
   chmod +x ~/.mcp/servers/mcp-access/src/mcp_access_server.py
   ```

2. **Dependencias faltantes:**
   ```bash
   pip install -r ~/.mcp/servers/mcp-access/requirements.txt
   ```

3. **Configuración incorrecta:**
   ```bash
   # Regenerar configuración
   python ~/.mcp/servers/mcp-access/auto_setup.py REPO_URL
   ```

---

## 📋 **Checklist de Sincronización**

- [ ] ✅ Repositorio GitHub creado
- [ ] ✅ Scripts de sincronización descargados
- [ ] ✅ Dependencias instaladas en todas las máquinas
- [ ] ✅ Configuración de Trae actualizada
- [ ] ✅ MCP funcionando en todas las máquinas
- [ ] ✅ Automatización configurada (opcional)

---

## 🎯 **Comandos Rápidos**

```bash
# Sincronización rápida (cualquier plataforma)
python auto_setup.py https://github.com/TU_USUARIO/mcp-access-database.git

# Actualización rápida
cd ~/.mcp/servers/mcp-access && git pull && pip install -r requirements.txt

# Verificación rápida
python ~/.mcp/servers/mcp-access/src/mcp_access_server.py --version
```

¡Con esta configuración tendrás tu MCP sincronizado automáticamente en todas tus máquinas! 🚀