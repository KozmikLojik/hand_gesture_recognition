import cv2
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier

# Initialize modules
detector = HandDetector()
classifier = GestureClassifier()

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Detect hand and draw landmarks
    frame = detector.find_hands(frame)

    # Get landmarks and classify gesture
    landmarks = detector.get_landmarks()
    gesture = classifier.classify(landmarks)

    # Display gesture on screen
    cv2.putText(frame, f'Gesture: {gesture}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
