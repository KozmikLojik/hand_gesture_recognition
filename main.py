import cv2
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier

detector = HandDetector()
classifier = GestureClassifier()

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = detector.find_hands(frame)
    landmarks = detector.get_landmarks()
    gesture = classifier.classify(landmarks)

    classifier.trigger_action(gesture)
    classifier.control_mouse(landmarks)

    cv2.putText(frame, f'Gesture: {gesture}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
