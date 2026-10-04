import cv2

from gesture_classifier import GestureClassifier
from hand_detector import HandDetector


def main():
    detector = HandDetector()
    classifier = GestureClassifier()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        detector.close()
        raise RuntimeError("Could not open the default camera. Check camera access and try again.")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Camera frame could not be read; stopping gesture recognition.")
                break

            frame = detector.find_hands(frame)
            landmarks = detector.get_landmarks()
            gesture = classifier.classify(landmarks)
            classifier.trigger_action(gesture)
            classifier.control_mouse(landmarks)

            cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Hand Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
