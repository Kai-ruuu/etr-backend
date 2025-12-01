@echo off
cd /d "%~dp0"

call .\venv\scripts\activate
cd app
fastapi dev main.py --host localhost