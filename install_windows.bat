@echo off
setlocal
cd /d "%~dp0"

title AYRA-1 Installer

echo ==========================================
echo          AYRA-1 WINDOWS INSTALLER
echo ==========================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.9 or newer and try again.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Creating AYRA-1 virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Could not create the virtual environment.
        pause
        exit /b 1
    )
)

echo.
echo Updating pip...
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
    echo.
    echo ERROR: Could not update pip.
    pause
    exit /b 1
)

echo.
echo Installing AYRA-1 dependencies...
.venv\Scripts\python.exe -m pip install --upgrade --force-reinstall -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo Verifying installation...
.venv\Scripts\python.exe -c "import cv2; from pathlib import Path; print('OpenCV:', cv2.__version__); print('Face model:', Path('models/haarcascade_frontalface_default.xml').exists()); print('Eye model:', Path('models/haarcascade_eye_tree_eyeglasses.xml').exists())"
if errorlevel 1 (
    echo.
    echo ERROR: AYRA-1 verification failed.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo       AYRA-1 INSTALLATION COMPLETE
echo ==========================================
echo.
echo Start the project with:
echo   run_ayra1.bat
echo.
pause
