@echo off
REM Asociación 31 DE ENERO - doble clic para abrir el sistema (ventana interna, sin URLs)
cd /d "%~dp0"
python -m pip install -q -r requirements.txt
start /min "" pythonw escritorio.py
