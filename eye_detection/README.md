# AYRA-1 Eye Closure Detection

AYRA-1 is a **standalone Windows laptop** eye-closure detection prototype.

The project deliberately keeps the required setup small and self-contained. The OpenCV Haar-cascade models are stored inside the repository, so AYRA-1 does **not** depend on `cv2.data` containing those files.

## Features

- Laptop webcam
- Windows + Python
- OpenCV face detection
- OpenCV eye detection
- Configurable eye-closure delay
- Repeating Windows alarm using built-in `winsound`
- No pygame
- No MediaPipe
- No Raspberry Pi
- No GPIO
- No external buzzer
- No audio file required
- Bundled detector models
- Command-line camera and delay options
- Press **Q** to quit

## Requirements

- Windows 10/11
- Python 3.9+
- Working webcam

AYRA-1 uses OpenCV 4.13.0.92, which is available as a Windows x86-64 wheel using the stable CPython ABI.

## Recommended installation

Use the included installer so AYRA-1 gets its own virtual environment instead of modifying your global Python installation.

From the repository root, double-click:

```text
install_windows.bat
```

Or run:

```powershell
.\install_windows.bat
```

The installer creates:

```text
.venv\
```

and installs the exact dependency from `requirements.txt`.

## Run

After installation:

```powershell
.\run_ayra1.bat
```

Or:

```powershell
.\.venv\Scripts\python.exe eye_detection\eye_buzzer.py
```

## Test the alarm

1. Start AYRA-1.
2. Keep your face in the webcam view.
3. Close your eyes.
4. Keep them closed for about **1.5 seconds**.
5. The status changes to `EYES CLOSED - WAKE UP!`.
6. A repeating Windows beep starts.
7. Open your eyes and the alarm stops.

## Configuration

The default settings are:

```text
Camera index: 0
Alarm delay : 1.5 seconds
```

### Use another webcam

```powershell
.\.venv\Scripts\python.exe eye_detection\eye_buzzer.py --camera 1
```

### Change the alarm delay

For a 2-second delay:

```powershell
.\.venv\Scripts\python.exe eye_detection\eye_buzzer.py --delay 2
```

You can combine them:

```powershell
.\.venv\Scripts\python.exe eye_detection\eye_buzzer.py --camera 1 --delay 2
```

## Project structure

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

## Detection flow

```text
Laptop Webcam
      |
      v
OpenCV Face Detection
      |
      v
OpenCV Eye Detection
      |
      v
Eye-not-detected Timer
      |
      v
Windows winsound Alarm
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'gpiozero'`

That message comes from the old Raspberry Pi version.

Make sure you are using the current AYRA-1 `eye_detection\eye_buzzer.py`. The current version does **not** import `gpiozero`.

### Haar-cascade file error

The current project stores the detector XML files under:

```text
models/
```

Therefore it no longer depends on:

```text
cv2.data.haarcascades
```

### OpenCV version is wrong

The project requires:

```text
opencv-python==4.13.0.92
```

Run the installer again:

```powershell
.\install_windows.bat
```

Then check:

```powershell
.\.venv\Scripts\python.exe -c "import cv2; print(cv2.__version__)"
```

Expected:

```text
4.13.0
```

### Camera does not open

Check Windows:

**Settings -> Privacy & security -> Camera**

Enable camera access and desktop-app camera access.

Also close Teams, Zoom, Discord, browsers, or other software currently using the webcam.

### Detection is poor

Haar-cascade detection works best with:

- Face looking generally toward the camera
- Good front lighting
- Reasonably clear webcam image
- Minimal extreme head rotation

This is a prototype, so false detections are possible.

> AYRA-1 is for learning and experimentation. It is not a safety-certified driver-monitoring system and should not be relied upon while driving.
