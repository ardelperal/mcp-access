@echo off
REM ============================================================================
REM MCP Access Database - Instalador Principal
REM ============================================================================
REM Este script proporciona una interfaz unificada para instalar y configurar
REM el MCP Access Database con detección automática de proxy.
REM ============================================================================

setlocal enabledelayedexpansion
title MCP Access Database - Instalador Principal

echo.
echo ============================================================================
echo                    MCP ACCESS DATABASE - INSTALADOR
echo ============================================================================
echo.
echo Este instalador configurará automáticamente el MCP Access Database
echo con detección inteligente de proxy para entornos corporativos.
echo.

:MENU
echo Seleccione una opción:
echo.
echo [1] Instalación Completa (Recomendado)
echo     - Detección automática de proxy
echo     - Configuración global de Trae
echo     - Verificación de dependencias
echo.
echo [2] Instalación Rápida
echo     - Configuración básica sin verificaciones
echo.
echo [3] Solo Configurar Proxy
echo     - Detectar y configurar proxy únicamente
echo.
echo [4] Herramientas de Diagnóstico
echo     - Probar conectividad pip
echo     - Verificar configuración
echo.
echo [5] Salir
echo.
set /p choice="Ingrese su opción (1-5): "

if "%choice%"=="1" goto FULL_INSTALL
if "%choice%"=="2" goto QUICK_INSTALL
if "%choice%"=="3" goto PROXY_ONLY
if "%choice%"=="4" goto DIAGNOSTICS
if "%choice%"=="5" goto EXIT
echo Opción inválida. Intente nuevamente.
goto MENU

:FULL_INSTALL
echo.
echo ============================================================================
echo                        INSTALACIÓN COMPLETA
echo ============================================================================
echo.
echo Ejecutando instalación completa con detección automática de proxy...
echo.
call "scripts\setup\setup_with_proxy_detection.bat"
goto END

:QUICK_INSTALL
echo.
echo ============================================================================
echo                        INSTALACIÓN RÁPIDA
echo ============================================================================
echo.
echo Ejecutando instalación rápida...
echo.
call "scripts\setup\quick_setup.bat"
goto END

:PROXY_ONLY
echo.
echo ============================================================================
echo                     CONFIGURACIÓN DE PROXY
echo ============================================================================
echo.
echo Detectando y configurando proxy...
echo.
python "scripts\utils\detect_proxy.py"
goto END

:DIAGNOSTICS
echo.
echo ============================================================================
echo                    HERRAMIENTAS DE DIAGNÓSTICO
echo ============================================================================
echo.
echo [1] Probar pip install
echo [2] Verificar detección de Ivanti
echo [3] Resumen de configuración
echo [4] Volver al menú principal
echo.
set /p diag_choice="Seleccione diagnóstico (1-4): "

if "%diag_choice%"=="1" (
    echo.
    echo Probando pip install...
    python "tools\test_pip_install.py"
    pause
    goto DIAGNOSTICS
)
if "%diag_choice%"=="2" (
    echo.
    echo Verificando detección de Ivanti...
    python "tools\test_ivanti_detection.py"
    pause
    goto DIAGNOSTICS
)
if "%diag_choice%"=="3" (
    echo.
    echo Mostrando resumen de configuración...
    python "tools\test_final_summary.py"
    pause
    goto DIAGNOSTICS
)
if "%diag_choice%"=="4" goto MENU

echo Opción inválida.
goto DIAGNOSTICS

:END
echo.
echo ============================================================================
echo                            INSTALACIÓN COMPLETADA
echo ============================================================================
echo.
echo El MCP Access Database ha sido configurado exitosamente.
echo.
echo Próximos pasos:
echo 1. Reiniciar Trae AI para cargar la nueva configuración
echo 2. Verificar que el servidor MCP aparece en la configuración de Trae
echo 3. Probar la funcionalidad con comandos MCP
echo.
echo Para usar el servidor MCP:
echo 1. Abrir Trae AI
echo 2. Verificar configuracion en MCP Servers
echo 3. El servidor estara disponible como 'mcp-access'
echo.
pause
goto EXIT

:EXIT
echo.
echo Gracias por usar MCP Access Database!
exit /b 0