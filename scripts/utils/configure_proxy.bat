@echo off
echo 🌐 Configurando variables de entorno para proxy corporativo...
echo.

REM Configurar proxy para HTTP y HTTPS
set HTTP_PROXY=http://proxy.empresa.com:8080
set HTTPS_PROXY=http://proxy.empresa.com:8080
set http_proxy=http://proxy.empresa.com:8080
set https_proxy=http://proxy.empresa.com:8080

REM Configurar exclusiones para localhost y redes locales
set NO_PROXY=localhost,127.0.0.1,*.local,10.*,192.168.*,172.16.*,172.17.*,172.18.*,172.19.*,172.20.*,172.21.*,172.22.*,172.23.*,172.24.*,172.25.*,172.26.*,172.27.*,172.28.*,172.29.*,172.30.*,172.31.*
set no_proxy=localhost,127.0.0.1,*.local,10.*,192.168.*,172.16.*,172.17.*,172.18.*,172.19.*,172.20.*,172.21.*,172.22.*,172.23.*,172.24.*,172.25.*,172.26.*,172.27.*,172.28.*,172.29.*,172.30.*,172.31.*

echo ✅ Variables de entorno configuradas:
echo    HTTP_PROXY=%HTTP_PROXY%
echo    HTTPS_PROXY=%HTTPS_PROXY%
echo    NO_PROXY=%NO_PROXY%
echo.

REM Configurar git para usar proxy
echo 🔧 Configurando Git para usar proxy...
git config --global http.proxy %HTTP_PROXY%
git config --global https.proxy %HTTPS_PROXY%
echo ✅ Git configurado para usar proxy

echo.
echo 🔧 Configurando pip para usar proxy...
pip config set global.proxy %HTTP_PROXY%
echo ✅ pip configurado para usar proxy

echo.
echo 🎉 Configuración de proxy completada!
echo.
echo 📋 Para usar estas configuraciones en esta sesión:
echo    - Las variables ya están configuradas en esta ventana
echo    - Git y pip están configurados globalmente
echo.
echo 🔄 Para hacer permanente en el sistema:
echo    - Ir a Panel de Control ^> Sistema ^> Configuración avanzada del sistema
echo    - Variables de entorno ^> Variables del sistema
echo    - Agregar las variables HTTP_PROXY, HTTPS_PROXY, NO_PROXY
echo.
echo ⚠️  NOTA: Ajusta la URL del proxy según tu configuración corporativa
echo    Ejemplo: http://usuario:contraseña@proxy.empresa.com:8080
echo.
pause