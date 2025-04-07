import HandTrackingModule as htm
import cv2
import numpy as np
import time
import pyautogui
import math
import subprocess

def set_volume(volume_level):
    if 0 <= volume_level <= 100:
        subprocess.run(["osascript", "-e", f"set volume output volume {volume_level}"])

#VARIABLES
wCam, hCam = 1920, 1080
frameR = 100
smoothening = 4
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
vol = 0
volBar = 400


cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScreen, hScreen = pyautogui.size()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)
    
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        
        # print(x1, y1, x2, y2)
    
        fingers = detector.fingersUp()
        # print(fingers)
        
        #VOLUME CONTROL
        if fingers[0] == 1 and fingers[1] == 1:
            length, img, infoLine = detector.findDistance(4, 8, img)
            vol = np.interp(length, [60, 400], [0, 100])
            volBar = np.interp(length, [60, 400], [400, 150])
            set_volume(vol)
            
        #MOUSE CONTROL
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:
            cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (0, 255, 255), 2)
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScreen))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            
            pyautogui.moveTo(clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        
        #MOUSE CLICK    
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, infoLine = detector.findDistance(8, 12, img)
            if length < 70:
                cv2.circle(img, (infoLine[4], infoLine[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
    #VOLUME BAR
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(vol)}%', (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)            
    
    # FPS
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)