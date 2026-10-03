# AYRA-1 Eye Closure Detection

Laptop-only eye closure detection module.

## Features

- Uses the laptop webcam
- MediaPipe Face Mesh eye landmarks
- Eye Aspect Ratio (EAR) based detection
- Ignores normal short blinks
- Plays an alarm through laptop speakers after prolonged eye closure
- Press **Q** to quit

## Run

From the repository root:

```bash
pip install -r requirements.txt
python eye_detection/eye_buzzer.py
```

Place an `alarm.wav` file inside this directory before running.

## Configuration

Edit `eye_buzzer.py`:

```python
EAR_THRESHOLD = 0.20
CLOSED_TIME = 1.5
```

Lower the EAR threshold if it triggers too easily; raise it if closed eyes are not detected reliably.

> This is a prototype and is not a safety-certified driver monitoring system.
