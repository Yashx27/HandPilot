import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import speech_recognition as sr
import threading

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Voice recognition setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Control variables
click_delay = 0.4
last_click_time = 0
voice_delay = 3
last_voice_time = 0
voice_active = False  # For avoiding multiple triggers
status_message = ""
status_timer = 0

# Utility functions
def distance(p1, p2):
    return np.hypot(p2[0] - p1[0], p2[1] - p1[1])

def speak_to_type():
    global voice_active, status_message, status_timer
    voice_active = True
    status_message = "Voice Typing Started. Speak now..."
    status_timer = time.time()

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            command = recognizer.recognize_google(audio)
            pyautogui.write(command + ' ')  # Add space after text
            status_message = f"Typed: {command}"
    except sr.WaitTimeoutError:
        status_message = "No speech detected. Try again."
    except sr.UnknownValueError:
        status_message = "Could not understand. Speak clearly."
    except Exception as e:
        status_message = f"Voice Typing Error: {str(e)}"

    status_timer = time.time()
    voice_active = False

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    lm_list = []

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = img.shape
        for id, lm in enumerate(hand_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((id, cx, cy))
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    if lm_list:
        # Get landmarks
        x_index, y_index = lm_list[8][1:]   # Index finger tip
        x_thumb, y_thumb = lm_list[4][1:]   # Thumb tip
        x_ring, y_ring = lm_list[16][1:]    # Ring finger tip

        # Cursor movement
        screen_w, screen_h = pyautogui.size()
        cursor_x = np.interp(x_index, [100, 1180], [0, screen_w])
        cursor_y = np.interp(y_index, [100, 700], [0, screen_h])
        pyautogui.moveTo(cursor_x, cursor_y)

        # Left Click
        if distance((x_index, y_index), (x_thumb, y_thumb)) < 35 and (time.time() - last_click_time) > click_delay:
            last_click_time = time.time()
            pyautogui.click()
            status_message = "Left Click"
            status_timer = time.time()

        # Voice Typing trigger
        if distance((x_ring, y_ring), (x_thumb, y_thumb)) < 35 and (time.time() - last_voice_time) > voice_delay and not voice_active:
            last_voice_time = time.time()
            threading.Thread(target=speak_to_type).start()

    # Display status message on screen for 4 seconds
    if status_message and (time.time() - status_timer) < 4:
        cv2.putText(img, status_message, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Display window
    cv2.imshow("Voice Typing", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
