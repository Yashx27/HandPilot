import cv2
import time
import numpy as np
import mediapipe as mp
from pynput.mouse import Button, Controller
from screeninfo import get_monitors

# Init mouse
mouse = Controller()

# Webcam config
wCam, hCam = 640, 480
frameR = 100
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Get screen size
screen = get_monitors()[0]
screenW, screenH = screen.width, screen.height

# Mediapipe setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

def findHandLandmarks(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
    return lmList

def fingersUp(lmList):
    fingers = []
    if lmList[4][1] < lmList[3][1]:  # Thumb
        fingers.append(1)
    else:
        fingers.append(0)

    tips = [8, 12, 16, 20]  # Index to pinky
    for tip in tips:
        if lmList[tip][2] < lmList[tip - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

prev_time = 0

try:
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        lmList = findHandLandmarks(img)

        if lmList:
            x1, y1 = lmList[8][1], lmList[8][2]  # Index
            x2, y2 = lmList[12][1], lmList[12][2]  # Middle

            h, w, _ = img.shape
            cv2.rectangle(img, (frameR, frameR), (w - frameR, h - frameR), (255, 0, 255), 2)

            fingers = fingersUp(lmList)

            # Move mouse: only index finger up
            if fingers == [0, 1, 0, 0, 0]:
                x3 = np.interp(x1, (frameR, w - frameR), (0, screenW))
                y3 = np.interp(y1, (frameR, h - frameR), (0, screenH))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                if 0 <= clocX <= screenW and 0 <= clocY <= screenH:
                    mouse.position = (clocX, clocY)
                    plocX, plocY = clocX, clocY

                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            # Left Click: Index + Thumb close
            if fingers[0] == 1 and fingers[1] == 1 and sum(fingers) == 2:
                x_thumb, y_thumb = lmList[4][1], lmList[4][2]
                length = np.hypot(x_thumb - x1, y_thumb - y1)
                if length < 40:
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    mouse.click(Button.left, 1)
                    time.sleep(0.2)

            # Right Click: Thumb + Pinky
            if fingers[0] == 1 and fingers[4] == 1 and sum(fingers) == 2:
                mouse.click(Button.right, 1)
                time.sleep(0.2)

            # Scroll using Thumbs Up / Down
            if fingers == [1, 0, 0, 0, 0]:
                thumb_tip_y = lmList[4][2]
                thumb_base_y = lmList[3][2]

                # Thumbs Up: tip higher than base
                if thumb_tip_y < thumb_base_y:
                    mouse.scroll(0, 2)  # Scroll up
                    cv2.putText(img, "Scroll Up", (20, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    time.sleep(0.3)

                # Thumbs Down: tip lower than base
                elif thumb_tip_y > thumb_base_y:
                    mouse.scroll(0, -2)  # Scroll down
                    cv2.putText(img, "Scroll Down", (20, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    time.sleep(0.3)

        # FPS counter
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if curr_time != prev_time else 0
        prev_time = curr_time
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Gesture Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print("[ERROR]", e)
    import traceback
    traceback.print_exc()

cap.release()
cv2.destroyAllWindows()
