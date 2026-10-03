import cv2
import time
import threading
import winsound

# -----------------------------
# AYRA-1 Configuration
# -----------------------------
CLOSED_TIME = 1.5          # Seconds before alarm starts
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 5

# OpenCV ships these Haar Cascade files with the package.
FACE_CASCADE_FILE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
EYE_CASCADE_FILE = cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"


class AlarmController:
    """Non-blocking repeating Windows beep."""

    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = None
        self._lock = threading.Lock()
        self.active = False

    def _run(self):
        while not self._stop_event.is_set():
            try:
                winsound.Beep(1800, 350)
            except RuntimeError:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

            if self._stop_event.wait(0.15):
                break

    def start(self):
        with self._lock:
            if self.active:
                return

            self.active = True
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._run,
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


def main():
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_FILE)
    eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_FILE)

    if face_cascade.empty():
        raise RuntimeError("Could not load the OpenCV face detector.")

    if eye_cascade.empty():
        raise RuntimeError("Could not load the OpenCV eye detector.")

    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        raise RuntimeError("Could not open webcam. Check camera permissions.")

    closed_start_time = None
    alarm = AlarmController()

    print("===================================")
    print("        AYRA-1 EYE DETECTION")
    print("===================================")
    print("Camera started. Press Q to exit.")
    print("Close your eyes for 1.5 seconds to test the alarm.")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                continue

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
                x, y, w, h = max(faces, key=lambda box: box[2] * box[3])

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

                # Eyes are normally located in the upper part of the face.
                eye_region_height = int(h * 0.60)
                eye_gray = gray[y:y + eye_region_height, x:x + w]

                eyes = eye_cascade.detectMultiScale(
                    eye_gray,
                    scaleFactor=EYE_SCALE_FACTOR,
                    minNeighbors=EYE_MIN_NEIGHBORS,
                    minSize=(20, 20),
                )

                # Draw detected eyes.
                for ex, ey, ew, eh in eyes[:4]:
                    cv2.rectangle(
                        frame,
                        (x + ex, y + ey),
                        (x + ex + ew, y + ey + eh),
                        (255, 255, 255),
                        2,
                    )

                if len(eyes) > 0:
                    # At least one eye detected -> treat as open.
                    status = "EYES OPEN"
                    closed_start_time = None
                    alarm.stop()
                else:
                    # No eye detected continuously for CLOSED_TIME -> alarm.
                    if closed_start_time is None:
                        closed_start_time = time.monotonic()

                    closed_duration = time.monotonic() - closed_start_time
                    status = f"EYES CLOSED: {closed_duration:.1f}s"

                    if closed_duration >= CLOSED_TIME:
                        status = "EYES CLOSED - WAKE UP!"
                        alarm.start()
            else:
                # Do not alarm when the face disappears from the camera.
                closed_start_time = None
                alarm.stop()

            cv2.putText(
                frame,
                status,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255) if alarm.active else (255, 255, 255),
                2,
            )

            if alarm.active:
                cv2.putText(
                    frame,
                    "WAKE UP!",
                    (width := frame.shape[1] // 2 - 120, frame.shape[0] // 2),
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
