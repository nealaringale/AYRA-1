@echo off
title AYRA-1 Eye Detection

echo ===================================
echo        AYRA-1 EYE DETECTION
echo ===================================
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Starting AYRA-1...
echo Press Q in the camera window to exit.
echo.

python eye_detection\eye_buzzer.py

if errorlevel 1 (
    echo.
    echo AYRA-1 stopped with an error.
    pause
)

