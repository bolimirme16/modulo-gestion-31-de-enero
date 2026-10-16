@echo off
REM Verificación previa (ejecutar una vez en el PC de la secretaria)
cd /d "%~dp0"
echo === 1. Python ===
python --version || (echo FALTA PYTHON 3.10+ - descargarlo gratis de python.org & pause & exit /b 1)
echo.
echo === 2. WebView2 (ventana interna) ===
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" /v pv 2>nul && (echo WebView2 OK) || (echo AVISO: instalar WebView2 gratis de Microsoft - el sistema usara Edge modo app mientras tanto)
echo.
echo === 3. Dependencias ===
python -m pip install -r requirements.txt || (echo ERROR instalando dependencias & pause & exit /b 1)
echo.
echo === 4. Prueba rapida del sistema ===
python -c "import sys; sys.path.insert(0,'.'); import app; app.init_db(); print('BD OK - version', app.VERSION)"
echo.
echo TODO LISTO. Use iniciar.bat para abrir el sistema.
pause
