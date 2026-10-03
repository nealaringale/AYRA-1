# AYRA-1

AYRA-1 is a laptop-based computer-vision project for detecting prolonged eye closure and triggering an audible wake-up alarm.

## Eye Closure Detection

The current implementation is designed for Windows and uses OpenCV for face/eye detection plus Python's built-in `winsound` module for the alarm.

### Requirements

- Windows laptop/PC
- Python 3.14
- Working webcam

### Install

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run

```powershell
python eye_detection\eye_buzzer.py
```

Press **Q** to exit.

### Detection flow

```
Webcam -> OpenCV Face Detection -> Eye Detection -> Closure Timer -> Windows Beep
```

No Raspberry Pi, GPIO, pygame, MediaPipe, or external buzzer hardware is required.

> Prototype only; not a safety-certified driver monitoring system.
