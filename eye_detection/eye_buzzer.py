from pathlib import Path
import argparse
import cv2
import threading
import time
import winsound

# ============================================================
# AYRA-1 | Laptop Eye Closure Detection
# Windows + Python + OpenCV
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"

FACE_CASCADE_FILE = MODEL_DIR / "haarcascade_frontalface_default.xml"
EYE_CASCADE_FILE = MODEL_DIR / "haarcascade_eye_tree_eyeglasses.xml"

DEFAULT_CLOSED_TIME = 1.5
DEFAULT_CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 5


class AlarmController:
    """Play a repeating Windows alarm without blocking video processing."""

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


def parse_args():
    parser = argparse.ArgumentParser(
        description="AYRA-1 laptop eye-closure detection"
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=DEFAULT_CAMERA_INDEX,
        help="Webcam index (default: 0)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_CLOSED_TIME,
        help="Seconds before the alarm starts (default: 1.5)",
    )
    args = parser.parse_args()

    if args.delay <= 0:
        parser.error("--delay must be greater than 0")

    if args.camera < 0:
        parser.error("--camera must be 0 or greater")

    return args


def load_detector(path: Path, name: str):
    if not path.exists():
        raise FileNotFoundError(
            f"AYRA-1 model file is missing: {path}\n"
            "Make sure you downloaded/cloned the complete repository."
        )

    detector = cv2.CascadeClassifier(str(path))

    if detector.empty():
        raise RuntimeError(
            f"OpenCV could not load the AYRA-1 {name} detector:\n{path}"
        )

    return detector


def open_camera(camera_index: int):
    # DirectShow usually gives better behavior on Windows.
    camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        raise RuntimeError(
            f"Could not open webcam {camera_index}.\n"
            "Check Windows camera permission and close any other app "
            "using the webcam."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    return camera


def draw_text(frame, text, position, alarm_active=False, scale=0.75):
    color = (0, 0, 255) if alarm_active else (255, 255, 255)

    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        2,
        cv2.LINE_AA,
    )


def main():
    args = parse_args()

    face_cascade = load_detector(FACE_CASCADE_FILE, "face")
    eye_cascade = load_detector(EYE_CASCADE_FILE, "eye")

    camera = open_camera(args.camera)
    alarm = AlarmController()

    closed_start_time = None

    print("===================================")
    print("        AYRA-1 EYE DETECTION")
    print("===================================")
    print(f"Camera index : {args.camera}")
    print(f"Alarm delay  : {args.delay:.1f} seconds")
    print("Camera started.")
    print("Press Q in the camera window to exit.")
    print("")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                draw_text(frame, "CAMERA FRAME ERROR", (20, 40), True)
                cv2.imshow("AYRA-1 | Eye Closure Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
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

                # Search only the upper portion of the detected face.
                eye_region_height = max(1, int(h * 0.60))
                eye_gray = gray[y:y + eye_region_height, x:x + w]

                eyes = eye_cascade.detectMultiScale(
                    eye_gray,
                    scaleFactor=EYE_SCALE_FACTOR,
                    minNeighbors=EYE_MIN_NEIGHBORS,
                    minSize=(20, 20),
                )

                # Keep only plausible eye detections in the upper face.
                valid_eyes = []
                for ex, ey, ew, eh in eyes:
                    eye_center_y = ey + eh / 2
                    if eye_center_y < eye_region_height * 0.90:
                        valid_eyes.append((ex, ey, ew, eh))

                for ex, ey, ew, eh in valid_eyes[:4]:
                    cv2.rectangle(
                        frame,
                        (x + ex, y + ey),
                        (x + ex + ew, y + ey + eh),
                        (255, 255, 255),
                        2,
                    )

                if valid_eyes:
                    status = "EYES OPEN"
                    closed_start_time = None
                    alarm.stop()
                else:
                    if closed_start_time is None:
                        closed_start_time = time.monotonic()

                    closed_duration = (
                        time.monotonic() - closed_start_time
                    )

                    status = f"EYES CLOSED?: {closed_duration:.1f}s"

                    if closed_duration >= args.delay:
                        status = "EYES CLOSED - WAKE UP!"
                        alarm.start()
            else:
                # A missing face is not treated as closed eyes.
                closed_start_time = None
                alarm.stop()

            height, width = frame.shape[:2]

            draw_text(
                frame,
                status,
                (20, 40),
                alarm_active=alarm.active,
            )

            draw_text(
                frame,
                f"Alarm delay: {args.delay:.1f}s",
                (20, 72),
                alarm_active=False,
                scale=0.55,
            )

            draw_text(
                frame,
                "Q = Quit",
                (20, height - 20),
                alarm_active=False,
                scale=0.55,
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
                    cv2.LINE_AA,
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
