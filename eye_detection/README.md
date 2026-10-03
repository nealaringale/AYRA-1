# AYRA-1 Eye Closure Detection

Laptop-only eye closure detection for Windows.

## Features

- Uses the laptop webcam
- OpenCV face and eye detection
- Detects prolonged eye closure using a time threshold
- Plays a repeating Windows beep after prolonged eye closure
- No pygame
- No MediaPipe
- No Raspberry Pi or GPIO hardware
- Press **Q** to quit

## Python compatibility

This version is designed for Windows and Python 3.14 using the current OpenCV package.

## Install

From the repository root:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python eye_detection\eye_buzzer.py
```

No `alarm.wav` file is required. AYRA-1 uses the built-in Windows `winsound` module.

## Configuration

Open `eye_detection/eye_buzzer.py` and adjust:

```python
CLOSED_TIME = 1.5
```

Increase this value if you want to tolerate longer eye closures before the alarm starts.

## Detection flow

```
Webcam -> OpenCV Face Detection -> OpenCV Eye Detection
       -> Eyes not detected continuously -> Windows alarm
```

> Prototype only; this is not a safety-certified driver monitoring system.
