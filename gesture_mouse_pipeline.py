import math
import time
from pathlib import Path

import cv2
import mediapipe as mp
import pyautogui


pyautogui.FAILSAFE = False

HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
)


class VirtualMousePipeline:
    def __init__(self) -> None:
        self.screen_width, self.screen_height = pyautogui.size()
        self.camera_width = 1280
        self.camera_height = 720
        self.frame_margin = 120
        self.smoothing = 6
        self.scroll_step = 110
        self.click_cooldown = 0.35
        self.last_click_time = 0.0
        self.last_scroll_time = 0.0
        self.previous_x = 0.0
        self.previous_y = 0.0
        self.current_x = 0.0
        self.current_y = 0.0
        self.running = True

        self.base_options = mp.tasks.BaseOptions(
            model_asset_path=str(Path("models") / "hand_landmarker.task")
        )
        self.hand_options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=self.base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.hand_landmarker = mp.tasks.vision.HandLandmarker.create_from_options(
            self.hand_options
        )

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open the default camera.")

    @staticmethod
    def _distance(point_a, point_b) -> float:
        return math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])

    def _extract_landmark_pixels(self, hand_landmarks):
        points = {}
        for idx, landmark in enumerate(hand_landmarks):
            points[idx] = (
                int(landmark.x * self.camera_width),
                int(landmark.y * self.camera_height),
            )
        return points

    def _draw_landmarks(self, frame, points):
        for start, end in HAND_CONNECTIONS:
            cv2.line(frame, points[start], points[end], (93, 203, 255), 2)
        for idx, point in points.items():
            radius = 10 if idx in (4, 8, 12) else 6
            color = (0, 255, 0) if idx in (4, 8, 12) else (255, 255, 255)
            cv2.circle(frame, point, radius, color, cv2.FILLED)

    def _move_cursor(self, index_tip):
        mapped_x = int(
            (index_tip[0] - self.frame_margin)
            * self.screen_width
            / (self.camera_width - 2 * self.frame_margin)
        )
        mapped_y = int(
            (index_tip[1] - self.frame_margin)
            * self.screen_height
            / (self.camera_height - 2 * self.frame_margin)
        )

        mapped_x = max(0, min(self.screen_width, mapped_x))
        mapped_y = max(0, min(self.screen_height, mapped_y))

        self.current_x = self.previous_x + (mapped_x - self.previous_x) / self.smoothing
        self.current_y = self.previous_y + (mapped_y - self.previous_y) / self.smoothing

        pyautogui.moveTo(self.screen_width - self.current_x, self.current_y)
        self.previous_x, self.previous_y = self.current_x, self.current_y

    def _handle_clicks(self, index_tip, middle_tip, thumb_tip):
        now = time.time()
        index_thumb_distance = self._distance(index_tip, thumb_tip)
        middle_thumb_distance = self._distance(middle_tip, thumb_tip)

        if index_thumb_distance < 35 and now - self.last_click_time > self.click_cooldown:
            pyautogui.click()
            self.last_click_time = now
            return "Left click"

        if middle_thumb_distance < 40 and now - self.last_click_time > self.click_cooldown:
            pyautogui.rightClick()
            self.last_click_time = now
            return "Right click"

        return "Tracking"

    def _handle_scroll(self, index_tip, middle_tip, index_base):
        now = time.time()
        fingers_close = self._distance(index_tip, middle_tip) < 30
        above_knuckle = index_tip[1] < index_base[1] - 40
        below_knuckle = index_tip[1] > index_base[1] + 40

        if fingers_close and now - self.last_scroll_time > 0.18:
            if above_knuckle:
                pyautogui.scroll(self.scroll_step)
                self.last_scroll_time = now
                return "Scroll up"
            if below_knuckle:
                pyautogui.scroll(-self.scroll_step)
                self.last_scroll_time = now
                return "Scroll down"

        return None

    def _draw_ui(self, frame, status_text):
        cv2.rectangle(
            frame,
            (self.frame_margin, self.frame_margin),
            (self.camera_width - self.frame_margin, self.camera_height - self.frame_margin),
            (76, 201, 240),
            2,
        )
        cv2.rectangle(frame, (20, 20), (430, 122), (18, 18, 18), -1)
        cv2.putText(
            frame,
            "Virtual Mouse Pipeline Active",
            (35, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Status: {status_text}",
            (35, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (76, 201, 240),
            2,
        )
        cv2.putText(
            frame,
            "Press Q, Esc, or click X once to close camera completely",
            (35, self.camera_height - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
        )

    def _window_closed(self) -> bool:
        return cv2.getWindowProperty("Virtual Mouse Pipeline", cv2.WND_PROP_VISIBLE) < 1

    def run(self):
        status_text = "Waiting for hand"
        cv2.namedWindow("Virtual Mouse Pipeline", cv2.WINDOW_NORMAL)

        try:
            while self.running:
                has_frame, frame = self.cap.read()
                if not has_frame:
                    status_text = "Camera frame unavailable"
                    break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                timestamp_ms = int(time.time() * 1000)
                result = self.hand_landmarker.detect_for_video(mp_image, timestamp_ms)

                if result.hand_landmarks:
                    hand_landmarks = result.hand_landmarks[0]
                    points = self._extract_landmark_pixels(hand_landmarks)

                    index_tip = points[8]
                    middle_tip = points[12]
                    thumb_tip = points[4]
                    index_base = points[5]

                    self._move_cursor(index_tip)
                    status_text = self._handle_clicks(index_tip, middle_tip, thumb_tip)

                    scroll_status = self._handle_scroll(index_tip, middle_tip, index_base)
                    if scroll_status:
                        status_text = scroll_status

                    self._draw_landmarks(frame, points)
                else:
                    status_text = "Waiting for hand"

                self._draw_ui(frame, status_text)
                cv2.imshow("Virtual Mouse Pipeline", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q") or key == 27:
                    self.running = False
                elif self._window_closed():
                    self.running = False
        finally:
            self.shutdown()

    def shutdown(self):
        if self.cap.isOpened():
            self.cap.release()
        self.hand_landmarker.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)


def run_virtual_mouse_pipeline():
    try:
        VirtualMousePipeline().run()
    except Exception as error:
        print(f"Application error: {error}")
