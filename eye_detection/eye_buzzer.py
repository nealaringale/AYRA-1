import cv2
import mediapipe as mp
import math
import time
import pygame

EAR_THRESHOLD = 0.20
CLOSED_TIME = 1.5
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
ALARM_FILE = "alarm.wav"

pygame.mixer.init()
pygame.mixer.music.load(ALARM_FILE)

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]


def distance(point1, point2):
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )


def calculate_ear(landmarks, eye, width, height):
    points = []
    for index in eye:
        landmark = landmarks[index]
        points.append((landmark.x * width, landmark.y * height))

    vertical_1 = distance(points[1], points[5])
    vertical_2 = distance(points[2], points[4])
    horizontal = distance(points[0], points[3])

    if horizontal == 0:
        return 0.0

    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def main():
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        raise RuntimeError("Could not open webcam.")

    eyes_closed = False
    closed_start_time = None
    alarm_active = False

    print("===================================")
    print("        AYRA-1 EYE DETECTION")
    print("===================================")
    print("Camera started. Press Q to exit.")

    try:
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:

            while True:
                success, frame = camera.read()
                if not success:
                    continue

                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb)

                status = "NO FACE"
                ear = 0.0

                if results.multi_face_landmarks:
                    landmarks = results.multi_face_landmarks[0].landmark

                    left_ear = calculate_ear(
                        landmarks, LEFT_EYE, width, height
                    )
                    right_ear = calculate_ear(
                        landmarks, RIGHT_EYE, width, height
                    )
                    ear = (left_ear + right_ear) / 2.0

                    if ear < EAR_THRESHOLD:
                        if not eyes_closed:
                            eyes_closed = True
                            closed_start_time = time.monotonic()

                        closed_duration = (
                            time.monotonic() - closed_start_time
                        )
                        status = f"EYES CLOSED: {closed_duration:.1f}s"

                        if closed_duration >= CLOSED_TIME:
                            status = "EYES CLOSED - WAKE UP!"

                            if not alarm_active:
                                pygame.mixer.music.play(-1)
                                alarm_active = True

                    else:
                        eyes_closed = False
                        closed_start_time = None
                        status = "EYES OPEN"

                        if alarm_active:
                            pygame.mixer.music.stop()
                            alarm_active = False

                    for index in LEFT_EYE + RIGHT_EYE:
                        point = landmarks[index]
                        x = int(point.x * width)
                        y = int(point.y * height)
                        cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)

                else:
                    eyes_closed = False
                    closed_start_time = None

                    if alarm_active:
                        pygame.mixer.music.stop()
                        alarm_active = False

                cv2.putText(
                    frame, f"EAR: {ear:.3f}", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
                )
                cv2.putText(
                    frame, status, (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255) if alarm_active else (255, 255, 255), 2
                )

                if alarm_active:
                    cv2.putText(
                        frame, "WAKE UP!",
                        (width // 2 - 120, height // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4
                    )

                cv2.imshow("AYRA-1 | Eye Closure Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        pygame.mixer.music.stop()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
