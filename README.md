# AYRA-1

**AYRA-1** is a standalone Windows-laptop computer-vision project for detecting prolonged eye closure and triggering an audible wake-up alarm.

## Current implementation

```text
Python
  |
  v
OpenCV
  |
  v
Laptop Webcam
  |
  v
Face Detection
  |
  v
Eye Detection
  |
  v
Closure Timer
  |
  v
Windows winsound Alarm
```

## Quick start

### 1. Install

Run:

```text
install_windows.bat
```

This creates a local `.venv` and installs the exact dependency version from `requirements.txt`.

### 2. Start

Run:

```text
run_ayra1.bat
```

Or from PowerShell:

```powershell
.\.venv\Scripts\python.exe eye_detection\eye_buzzer.py
```

Press **Q** to exit.

## Requirements

- Windows 10/11
- Python 3.9+
- Working webcam

No Raspberry Pi, GPIO, Arduino, ESP32, pygame, MediaPipe, or external buzzer is required.

## Repository structure

```text
AYRA-1/
|-- eye_detection/
|   |-- eye_buzzer.py
|   |-- README.md
|-- models/
|   |-- haarcascade_frontalface_default.xml
|   |-- haarcascade_eye_tree_eyeglasses.xml
|-- requirements.txt
|-- install_windows.bat
|-- run_ayra1.bat
|-- .gitignore
|-- README.md
```

## Why are the models in the repo?

AYRA-1 intentionally bundles its Haar-cascade XML files rather than loading them from the installed OpenCV package. This makes the project independent of the `cv2/data` contents of a particular wheel.

## Important

AYRA-1 is a prototype for learning and experimentation. It is not a safety-certified driver-monitoring system.
