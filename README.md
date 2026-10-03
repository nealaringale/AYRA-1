# AYRA-1

## Eye Closure Detection

AYRA-1 includes a laptop-only computer-vision module that uses the webcam to detect prolonged eye closure and plays an alarm through the laptop speakers.

### Run

```bash
pip install -r requirements.txt
python eye_detection/eye_buzzer.py
```

Put `alarm.wav` inside `eye_detection/`.

### Detection flow

```
Webcam -> MediaPipe -> Eye landmarks -> EAR -> Closed eyes -> Laptop alarm
```

This module requires no Raspberry Pi, GPIO, or external buzzer hardware.

> Prototype only; not a safety-certified driver monitoring system.
