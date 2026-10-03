@echo off
setlocal
cd /d "%~dp0"

title AYRA-1 Eye Detection

if not exist ".venv\Scripts\python.exe" (
    echo AYRA-1 is not installed yet.
    echo.
    echo Run install_windows.bat first.
    echo.
    pause
    exit /b 1
)

echo ===================================
echo        AYRA-1 EYE DETECTION
echo ===================================
echo.
echo Starting AYRA-1...
echo Press Q in the camera window to exit.
echo.

.venv\Scripts\python.exe eye_detection\eye_buzzer.py

if errorlevel 1 (
    echo.
    echo AYRA-1 stopped with an error.
    pause
)
