@echo off
chcp 65001 > nul
echo.
echo =====================================================
echo   UzRetro.uz - Python Saytni Ishga Tushurish
echo =====================================================
echo.

:: Python yo'lini topish
set PYTHON_CMD=

:: Birinchi oddiy python
python --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=python
    goto FOUND_PYTHON
)

:: Keyin AppData/Local/Programs
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    goto FOUND_PYTHON
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
    goto FOUND_PYTHON
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python310\python.exe
    goto FOUND_PYTHON
)

echo [XATO] Python topilmadi!
echo.
echo Python o'rnatish uchun:
echo   https://www.python.org/downloads/
echo   O'rnatishda "Add Python to PATH" ni belgilang!
echo.
pause
exit /b 1

:FOUND_PYTHON
echo [OK] Python topildi: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: Virtual environment
if not exist "venv" (
    echo Virtual environment yaratilmoqda...
    %PYTHON_CMD% -m venv venv
    echo [OK] Virtual environment tayyor
)

:: Aktivlashtirish
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo [XATO] Virtual environment aktivlashtirilmadi
    pause
    exit /b 1
)

:: Kutubxonalar
echo.
echo Kutubxonalar o'rnatilmoqda...
pip install -r requirements.txt -q
echo [OK] Kutubxonalar tayyor
echo.

:: Saytni ishga tushirish
echo =====================================================
echo   SAYT ISHGA TUSHDI!
echo.
echo   Brauzeringizda oching:
echo     http://localhost:5000         -- Sayt
echo     http://localhost:5000/admin   -- Admin Panel
echo.
echo   Admin kirish:
echo     Login: admin
echo     Parol: uzretro2024
echo.
echo   To'xtatish uchun: Ctrl+C
echo =====================================================
echo.

python app.py

pause
