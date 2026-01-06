
import cv2
import mediapipe as mp
import math

# -------------------- MediaPipe setup --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# -------------------- Helper functions --------------------
def palm_center(lm):
    """Compute palm center using MCP joints"""
    x = (lm[5].x + lm[9].x + lm[13].x + lm[17].x) / 4
    y = (lm[5].y + lm[9].y + lm[13].y + lm[17].y) / 4
    return x, y

def distance_xy(p, center):
    """2D distance between a landmark and palm center"""
    return math.sqrt((p.x - center[0])**2 + (p.y - center[1])**2)

# -------------------- Camera -------------------------------------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
       break
 
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    total_fingers = 0

    if result.multi_hand_landmarks and result.multi_handedness:

        for idx, (hand_landmarks, hand_info) in enumerate(
            zip(result.multi_hand_landmarks, result.multi_handedness)
        ):
            lm = hand_landmarks.landmark
            hand_label = hand_info.classification[0].label

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            finger_count = 0

            # -------------------- THUMB (PALM DISTANCE LOGIC) ---------------------------------------
            center = palm_center(lm)
            thumb_dist = distance_xy(lm[4], center)

            THUMB_OPEN_THRESH = 0.12 

            if thumb_dist > THUMB_OPEN_THRESH:
                finger_count += 1

            # -------------------- OTHER FINGERS (Y-AXIS LOGIC) --------------------------------------
            tips = [8, 12, 16, 20]
            joints = [6, 10, 14, 18]

            for tip, joint in zip(tips, joints):
                if lm[tip].y < lm[joint].y:
                    finger_count += 1

            total_fingers += finger_count

            # -------------------- PER-HAND DISPLAY ---------------------------------------
            cv2.putText(
                frame,
                f"{hand_label} hand: {finger_count}",
                (30, 100 + idx * 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 0),
                2
            )

    # -------------------- TOTAL DISPLAY --------------------------------------------------------------
    cv2.putText(
        frame,
        f"Total Fingers: {total_fingers}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    cv2.imshow("Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


