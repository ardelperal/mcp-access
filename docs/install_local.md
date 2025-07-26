# Instalación Local del MCP Access Server

## 📋 Pasos para Instalación Local

### 1. Preparar el Entorno

```bash
# Navegar al directorio del proyecto
cd c:\Users\adm1\Desktop\Proyectos\mcp-access

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Verificar Instalación

```bash
# Ejecutar el script de inicio para verificar
.\start.bat
# Seleccionar opción 2 (Ejecutar pruebas)
```

### 3. Configurar Cliente MCP

#### Para Claude Desktop:
1. Abrir: `%APPDATA%\Claude\claude_desktop_config.json`
2. Agregar la configuración:

```json
{
  "mcpServers": {
    "access-db": {
      "command": "python",
      "args": ["c:\\Users\\adm1\\Desktop\\Proyectos\\mcp-access\\src\\mcp_access_server.py"],
      "env": {
        "PYTHONPATH": "c:\\Users\\adm1\\Desktop\\Proyectos\\mcp-access\\src"
      }
    }
  }
}
```

#### Para otros clientes MCP:
Buscar el archivo de configuración correspondiente y usar la misma estructura.

### 4. Requisitos del Sistema

- **Python 3.8+** instalado y en PATH
- **Microsoft Access Database Engine** (para .accdb/.mdb)
  - Descargar: https://www.microsoft.com/en-us/download/details.aspx?id=54920
- **Permisos de lectura/escritura** en las bases de datos Access

### 5. Verificar Funcionamiento

1. **Reiniciar el cliente MCP** (Claude Desktop, etc.)
2. **Probar conexión:**
   ```
   Usar herramienta: connect_database
   Parámetros: {"database_path": "ruta_a_tu_base_datos.accdb"}
   ```

### 6. Troubleshooting

#### Error: "Python no encontrado"
```bash
# Verificar instalación de Python
python --version
# Si no funciona, reinstalar Python y agregar a PATH
```

#### Error: "Módulo mcp no encontrado"
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

#### Error: "No se puede conectar a Access"
- Verificar que Microsoft Access Database Engine esté instalado
- Comprobar permisos de archivo
- Usar rutas absolutas para las bases de datos

### 7. Configuración Avanzada

#### Variables de Entorno Opcionales:
```json
{
  "mcpServers": {
    "access-db": {
      "command": "python",
      "args": ["c:\\Users\\adm1\\Desktop\\Proyectos\\mcp-access\\src\\mcp_access_server.py"],
      "env": {
        "PYTHONPATH": "c:\\Users\\adm1\\Desktop\\Proyectos\\mcp-access\\src",
        "MCP_ACCESS_LOG_LEVEL": "INFO",
        "MCP_ACCESS_MAX_RESULTS": "1000"
      }
    }
  }
}
```

### 8. Instalación Global (Opcional)

Para una instalación más profesional:

1. **Crear directorio global:**
   ```bash
   mkdir "C:\Program Files\MCPServers\mcp-access"
   ```

2. **Copiar archivos:**
   ```bash
   xcopy "c:\Users\adm1\Desktop\Proyectos\mcp-access\*" "C:\Program Files\MCPServers\mcp-access\" /E /I
   ```

3. **Actualizar configuración:**
   ```json
   {
     "mcpServers": {
       "access-db": {
         "command": "python",
         "args": ["C:\\Program Files\\MCPServers\\mcp-access\\src\\mcp_access_server.py"],
         "env": {}
       }
     }
   }
   ```

## ✅ Verificación Final

Después de la instalación, deberías poder:
- Ver "access-db" en la lista de servidores MCP
- Usar las 11 herramientas disponibles
- Conectarte a bases de datos Access (.mdb/.accdb)
- Realizar operaciones CRUD completas

## 🆘 Soporte

Si encuentras problemas:
1. Revisar logs del cliente MCP
2. Ejecutar `.\start.bat` y seleccionar "Verificar configuración"
3. Consultar `docs/technical_documentation.md`