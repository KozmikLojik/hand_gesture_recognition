import pyautogui
import os
import time

pyautogui.FAILSAFE = True  # Keep fail-safe enabled for safety

class GestureClassifier:
    def __init__(self):
        self.finger_tips = [8, 12, 16, 20]
        self.thumb_tip = 4
        self.last_triggered = None

    def classify(self, landmarks):
        if not landmarks:
            return "No hand"

        hand_landmarks = landmarks[0].landmark
        fingers = []

        # Thumb
        if hand_landmarks[self.thumb_tip].x < hand_landmarks[self.thumb_tip - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for tip in self.finger_tips:
            if hand_landmarks[tip].y < hand_landmarks[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = sum(fingers)

        if total_fingers == 0:
            return "Rock"
        elif fingers == [0, 1, 1, 0, 0]:
            return "Scissors"
        elif fingers == [0, 1, 0, 0, 0]:
            return "Pointing"
        elif total_fingers >= 4:
            return "Waving"
        else:
            return "Unknown"

    def trigger_action(self, gesture):
        if gesture == self.last_triggered:
            return
        self.last_triggered = gesture
        print(f"Triggering action for: {gesture}")
        time.sleep(1)

        if gesture == "Scissors":
            pyautogui.screenshot("screenshot.png")
        elif gesture == "Rock":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif gesture == "Waving":
            pyautogui.hotkey('win', 'down')

    def control_mouse(self, landmarks):
        if not landmarks:
            return

        hand = landmarks[0].landmark
        index_tip = hand[8]
        thumb_tip = hand[4]

        screen_width, screen_height = pyautogui.size()
        x = int(index_tip.x * screen_width)
        y = int(index_tip.y * screen_height)

        # Clamp mouse position to avoid fail-safe corners
        x = max(10, min(screen_width - 10, x))
        y = max(10, min(screen_height - 10, y))

        pyautogui.moveTo(x, y)

        pinch_distance = abs(index_tip.x - thumb_tip.x) + abs(index_tip.y - thumb_tip.y)
        if pinch_distance < 0.05:
            pyautogui.click()

        fingers_up = sum([
            hand[8].y < hand[6].y,
            hand[12].y < hand[10].y,
            hand[16].y < hand[14].y,
            hand[20].y < hand[18].y
        ])
        if fingers_up >= 4:
            pyautogui.moveTo(screen_width // 2, screen_height // 2)
