import math

class GestureClassifier:
    def __init__(self):
        # Define landmark indices for fingertips
        self.finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        self.thumb_tip = 4

    def classify(self, landmarks):
        if not landmarks:
            return "No hand"

        hand_landmarks = landmarks[0].landmark

        # Count extended fingers
        fingers = []

        # Thumb: compare tip and base x-coordinates
        if hand_landmarks[self.thumb_tip].x < hand_landmarks[self.thumb_tip - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers: tip higher than lower joint (y-axis)
        for tip in self.finger_tips:
            if hand_landmarks[tip].y < hand_landmarks[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = sum(fingers)

        # Gesture logic
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
