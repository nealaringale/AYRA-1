import cv2
import threading
import time
import winsound

# ============================================================
# AYRA-1 | Laptop Eye Closure Detection
# Windows + Python + OpenCV
# ============================================================

# Time eyes must remain undetected before the alarm starts.
CLOSED_TIME = 1.5

# Default laptop webcam.
CAMERA_INDEX = 0

# Camera resolution.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# OpenCV Haar-cascade settings.
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 5

FACE_CASCADE_FILE = (
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
EYE_CASCADE_FILE = (
    cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"
)


class AlarmController:
    """Play a repeating Windows beep without blocking the camera loop."""

    def __init__(self):
        self.active = False
        self._stop_event = threading.Event()
        self._thread = None
        self._lock = threading.Lock()

    def _play(self):
        while not self._stop_event.is_set():
            try:
                winsound.Beep(1800, 350)
            except RuntimeError:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

            # Small gap between beeps.
            if self._stop_event.wait(0.15):
                break

    def start(self):
        with self._lock:
            if self.active:
                return

            self.active = True
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._play,
                name="AYRA-1-Alarm",
                daemon=True,
            )
            self._thread.start()

    def stop(self):
        with self._lock:
            if not self.active:
                return

            self.active = False
            self._stop_event.set()
            thread = self._thread
            self._thread = None

        if thread and thread.is_alive():
            thread.join(timeout=0.6)

    def close(self):
        self.stop()


def load_detector(path, name):
    detector = cv2.CascadeClassifier(path)

    if detector.empty():
        raise RuntimeError(f"Could not load OpenCV {name} detector.")

    return detector


def main():
    face_cascade = load_detector(FACE_CASCADE_FILE, "face")
    eye_cascade = load_detector(EYE_CASCADE_FILE, "eye")

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        raise RuntimeError(
            "Could not open webcam. Check Windows camera permissions "
            "and make sure another app is not using the camera."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    alarm = AlarmController()
    closed_start_time = None

    print("===================================")
    print("        AYRA-1 EYE DETECTION")
    print("===================================")
    print(f"Eye closure alarm delay: {CLOSED_TIME:.1f} seconds")
    print("Camera started. Press Q in the camera window to exit.")
    print("")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Warning: could not read a webcam frame.")
                continue

            # Mirror the camera image like a normal webcam preview.
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=FACE_SCALE_FACTOR,
                minNeighbors=FACE_MIN_NEIGHBORS,
                minSize=(100, 100),
            )

            status = "NO FACE"

            if len(faces) > 0:
                # Use the largest detected face.
                x, y, w, h = max(
                    faces,
                    key=lambda box: box[2] * box[3],
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (255, 255, 255),
                    2,
                )

                # Eyes are normally found in the upper 60% of the face.
                eye_region_height = int(h * 0.60)
                eye_gray = gray[y:y + eye_region_height, x:x + w]

                eyes = eye_cascade.detectMultiScale(
                    eye_gray,
                    scaleFactor=EYE_SCALE_FACTOR,
                    minNeighbors=EYE_MIN_NEIGHBORS,
                    minSize=(20, 20),
                )

                for ex, ey, ew, eh in eyes[:4]:
                    cv2.rectangle(
                        frame,
                        (x + ex, y + ey),
                        (x + ex + ew, y + ey + eh),
                        (255, 255, 255),
                        2,
                    )

                if len(eyes) > 0:
                    # Eye detected -> eyes are considered open.
                    status = "EYES OPEN"
                    closed_start_time = None
                    alarm.stop()
                else:
                    # No eye detected while a face is visible.
                    if closed_start_time is None:
                        closed_start_time = time.monotonic()

                    closed_duration = (
                        time.monotonic() - closed_start_time
                    )

                    status = f"EYES CLOSED: {closed_duration:.1f}s"

                    if closed_duration >= CLOSED_TIME:
                        status = "EYES CLOSED - WAKE UP!"
                        alarm.start()

            else:
                # Do not treat a missing face as closed eyes.
                closed_start_time = None
                alarm.stop()

            height, width = frame.shape[:2]

            cv2.putText(
                frame,
                status,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255) if alarm.active else (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                "Q = Quit",
                (20, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
            )

            if alarm.active:
                cv2.putText(
                    frame,
                    "WAKE UP!",
                    (width // 2 - 120, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (0, 0, 255),
                    4,
                )

            cv2.imshow("AYRA-1 | Eye Closure Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        alarm.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
