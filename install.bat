@echo off

echo === Instalacija ZODB Top Down Survival Shooter Projekta ===

REM 1. Virtualna okruženja
echo Kreiram virtualnu okruženja...
python -m venv venv

REM 2. Aktivacija
echo Aktiviram virtualnu okruženja...
call venv\Scripts\activate.bat

REM 3. Instalacija paketa
echo Instaliram pakete...
pip install -r requirements.txt

echo.
echo Instalacija je uspjesna!
echo.
echo Za pokretanje igre, izvrsit ce:
echo   venv\Scripts\activate.bat
echo   python src/main.py

pause
