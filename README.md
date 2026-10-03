# AYRA-1

**AYRA-1** is a standalone laptop computer-vision project for detecting prolonged eye closure and triggering an audible wake-up alarm.

## Current project

### Eye Closure Detection

Location:

```text
eye_detection/eye_buzzer.py
```

Technology:

- Python
- OpenCV
- Windows `winsound`
- Laptop webcam

### Install

From the repository root:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run

```powershell
python eye_detection\eye_buzzer.py
```

Or double-click:

```text
run_ayra1.bat
```

Press **Q** to exit the camera window.

## Project structure

```text
AYRA-1/
|-- eye_detection/
|   |-- eye_buzzer.py
|   |-- README.md
|-- requirements.txt
|-- run_ayra1.bat
|-- README.md
```

## Detection flow

```text
Webcam
  -> OpenCV Face Detection
  -> OpenCV Eye Detection
  -> Closure Timer
  -> Windows Alarm
```

## Hardware

This version is designed for a **normal Windows laptop**.

It does **not** require:

- Raspberry Pi
- GPIO
- External buzzer
- Arduino
- ESP32
- pygame
- MediaPipe
- `alarm.wav`

## Important

AYRA-1 is a prototype for learning and experimentation. It is not a safety-certified driver monitoring system.
