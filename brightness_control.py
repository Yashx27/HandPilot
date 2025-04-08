import cv2
import mediapipe as mp
import numpy as np
import math
import screen_brightness_control as sbc
import time

# MediaPipe hand setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if len(lmList) != 0:
        # Thumb tip (4) and index finger tip (8)
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Visuals
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # Distance between fingers
        length = math.hypot(x2 - x1, y2 - y1)

        # Map distance to brightness (0 to 100)
        brightness = np.interp(length, [20, 200], [0, 100])
        sbc.set_brightness(int(brightness))

        # Brightness bar
        bar = np.interp(length, [20, 200], [400, 150])
        cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 0), 3)
        cv2.rectangle(img, (50, int(bar)), (85, 400), (255, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(brightness)}%', (40, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display
    cv2.imshow("Brightness Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
