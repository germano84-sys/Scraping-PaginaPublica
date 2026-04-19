@echo off
echo Iniciando Scraper Web de Tabla de Posiciones...
echo.
cd /d "%~dp0"
if not exist ".venv" (
    echo Error: Entorno virtual no encontrado. Ejecuta primero: python -m venv .venv
    pause
    exit /b 1
)
call .\.venv\Scripts\activate
python -m uvicorn main:app --host 127.0.0.1 --port 8007 --reload
pause