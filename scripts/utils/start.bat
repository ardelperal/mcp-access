@echo off
title MCP Access Server - Inicio Rapido
color 0A

echo.
echo  ███╗   ███╗ ██████╗██████╗      █████╗  ██████╗ ██████╗███████╗███████╗███████╗
echo  ████╗ ████║██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝
echo  ██╔████╔██║██║     ██████╔╝    ███████║██║     ██║     █████╗  ███████╗███████╗
echo  ██║╚██╔╝██║██║     ██╔═══╝     ██╔══██║██║     ██║     ██╔══╝  ╚════██║╚════██║
echo  ██║ ╚═╝ ██║╚██████╗██║         ██║  ██║╚██████╗╚██████╗███████╗███████║███████║
echo  ╚═╝     ╚═╝ ╚═════╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝
echo.
echo                          Servidor MCP para Microsoft Access
echo                                    Version 1.0.0
echo.
echo ================================================================================

:MENU
echo.
echo Selecciona una opcion:
echo.
echo [1] Instalar dependencias
echo [2] Ejecutar pruebas
echo [3] Iniciar servidor MCP
echo [4] Ejecutar ejemplo interactivo
echo [5] Verificar configuracion
echo [6] Ver documentacion
echo [7] Salir
echo.
set /p choice="Ingresa tu opcion (1-7): "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto TEST
if "%choice%"=="3" goto START_SERVER
if "%choice%"=="4" goto EXAMPLE
if "%choice%"=="5" goto CHECK_CONFIG
if "%choice%"=="6" goto DOCS
if "%choice%"=="7" goto EXIT
goto MENU

:INSTALL
echo.
echo ================================================================================
echo  INSTALANDO DEPENDENCIAS
echo ================================================================================
echo.
echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instala Python 3.8+ desde python.org
    pause
    goto MENU
)

echo.
echo Instalando paquetes requeridos...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    goto MENU
) else (
    echo.
    echo ✅ Dependencias instaladas exitosamente!
    echo.
    echo IMPORTANTE: Asegurate de tener instalado Microsoft Access Database Engine:
    echo https://www.microsoft.com/en-us/download/details.aspx?id=54920
)
pause
goto MENU

:TEST
echo.
echo ================================================================================
echo  EJECUTANDO PRUEBAS
echo ================================================================================
echo.
python tests\test_mcp_access.py
pause
goto MENU

:START_SERVER
echo.
echo ================================================================================
echo  INICIANDO SERVIDOR MCP
echo ================================================================================
echo.
echo El servidor MCP se ejecutara en modo stdio.
echo Para detenerlo, presiona Ctrl+C
echo.
pause
python src\mcp_access_server.py
pause
goto MENU

:EXAMPLE
echo.
echo ================================================================================
echo  EJEMPLO INTERACTIVO
echo ================================================================================
echo.
python examples\test_mcp.py
pause
goto MENU

:CHECK_CONFIG
echo.
echo ================================================================================
echo  VERIFICANDO CONFIGURACION
echo ================================================================================
echo.

echo Verificando Python...
python --version
echo.

echo Verificando paquetes instalados...
pip show pyodbc 2>nul
if errorlevel 1 (
    echo ❌ pyodbc no instalado
) else (
    echo ✅ pyodbc instalado
)

pip show mcp 2>nul
if errorlevel 1 (
    echo ❌ mcp no instalado
) else (
    echo ✅ mcp instalado
)

echo.
echo Verificando drivers ODBC disponibles...
python -c "import pyodbc; drivers = pyodbc.drivers(); access_drivers = [d for d in drivers if 'Access' in d]; print('Drivers de Access encontrados:'); [print(f'  - {d}') for d in access_drivers] if access_drivers else print('  ❌ No se encontraron drivers de Access')" 2>nul

echo.
echo Verificando estructura del proyecto...
if exist "src\mcp_access_server.py" (
    echo ✅ Servidor principal encontrado
) else (
    echo ❌ Servidor principal no encontrado
)

if exist "src\config.py" (
    echo ✅ Archivo de configuracion encontrado
) else (
    echo ❌ Archivo de configuracion no encontrado
)

if exist "requirements.txt" (
    echo ✅ Archivo de dependencias encontrado
) else (
    echo ❌ Archivo de dependencias no encontrado
)

echo.
pause
goto MENU

:DOCS
echo.
echo ================================================================================
echo  DOCUMENTACION
echo ================================================================================
echo.
echo Abriendo documentacion...
echo.

if exist "docs\technical_documentation.md" (
    start notepad "docs\technical_documentation.md"
) else (
    echo ❌ Archivo de documentacion no encontrado
)

if exist "README.md" (
    echo.
    echo Contenido del README:
    echo ================================================================================
    type README.md
) else (
    echo ❌ README no encontrado
)

pause
goto MENU

:EXIT
echo.
echo ================================================================================
echo  GRACIAS POR USAR MCP ACCESS SERVER
echo ================================================================================
echo.
echo Para usar el servidor en produccion:
echo.
echo 1. Configura tu cliente MCP con la configuracion en mcp.json
echo 2. Ejecuta: python src\mcp_access_server.py
echo 3. Conecta a tu base de datos Access usando la herramienta connect_database
echo.
echo ¡Que tengas un excelente dia manipulando bases de datos Access!
echo.
pause
exit

:ERROR
echo.
echo ❌ Opcion invalida. Por favor selecciona una opcion del 1 al 7.
pause
goto MENU