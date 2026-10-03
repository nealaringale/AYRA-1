# AYRA-1 Eye Closure Detection

AYRA-1 is a **standalone Windows laptop** eye-closure detection prototype.

It uses the laptop webcam to detect a face, checks whether the eyes are visible, and starts a repeating Windows beep when the eyes have remained undetected for the configured time.

## Features

- Laptop webcam only
- Windows + Python
- OpenCV face and eye detection
- Ignores normal short blinks by using a time threshold
- Repeating alarm using Python's built-in `winsound`
- No pygame
- No MediaPipe
- No Raspberry Pi
- No GPIO
- No external buzzer
- No `alarm.wav` file required
- Press **Q** to quit

## Requirements

- Windows 10/11
- Python 3.9+
- Working webcam

Python 3.14 is supported by the current setup because AYRA-1 only requires OpenCV.

## Installation

Open PowerShell in the **AYRA-1 repository root** and run:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python eye_detection\eye_buzzer.py
```

Or double-click:

```text
run_ayra1.bat
```

## Test the alarm

1. Start AYRA-1.
2. Keep your face in the webcam view.
3. Close both eyes.
4. Keep them closed for about **1.5 seconds**.
5. The status will change to `EYES CLOSED - WAKE UP!`.
6. A repeating Windows beep will start.
7. Open your eyes and the alarm stops.

## Configuration

Edit `eye_detection\eye_buzzer.py`.

### Alarm delay

```python
CLOSED_TIME = 1.5
```

Example:

```python
CLOSED_TIME = 2.0
```

Use a larger value when normal blinks or brief eye-closure events are triggering the alarm.

### Webcam

If your laptop has multiple cameras:

```python
CAMERA_INDEX = 0
```

Try `1` or `2` for another camera.

## Detection flow

```
Laptop Webcam
      |
      v
OpenCV Face Detection
      |
      v
OpenCV Eye Detection
      |
      v
Eyes not detected for CLOSED_TIME
      |
      v
Windows winsound Alarm
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'gpiozero'`

You are running an old Raspberry Pi version of the project.

Download/clone the latest AYRA-1 repository and run the current file:

```powershell
python eye_detection\eye_buzzer.py
```

The current version does **not** import `gpiozero`.

### Camera does not open

Check Windows:

**Settings -> Privacy & security -> Camera**

Make sure camera access and desktop-app camera access are enabled.

Also close apps such as Teams, Zoom, Discord, or another camera application that may be using the webcam.

### Detection is poor

Good front-facing lighting improves Haar-cascade detection. Keep your face reasonably centered and avoid very dark rooms.

> Prototype only. This is not a safety-certified driver-monitoring system and should not be relied on while driving.
