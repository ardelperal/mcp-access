@echo off
echo ========================================
echo  MCP Access Server - Instalador
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Verificando drivers de Access...
echo ========================================

echo.
echo IMPORTANTE: Para que este MCP funcione necesitas tener instalado
echo el Microsoft Access Database Engine.
echo.
echo Si no lo tienes instalado, descargalo desde:
echo https://www.microsoft.com/en-us/download/details.aspx?id=54920
echo.
echo Presiona cualquier tecla para continuar...
pause >nul

echo.
echo ========================================
echo  Instalacion completada!
echo ========================================
echo.
echo Para usar el MCP Access Server:
echo.
echo 1. Configura tu cliente MCP con la configuracion en mcp.json
echo 2. Ejecuta: python src/mcp_access_server.py
echo 3. O ejecuta las pruebas: python examples/test_mcp.py
echo.
echo ¡Disfruta manipulando bases de datos Access con MCP!
echo.
pause