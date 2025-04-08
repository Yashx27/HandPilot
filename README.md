# 🖐️ Intuitive Control System (Gesture + Voice + GUI)

This project is a multifunctional human-computer interaction system using computer vision and speech recognition. It enables control of mouse, scrolling, volume, screen brightness, and more using **hand gestures**, **voice commands**, and a simple **GUI** interface.

---

## 🔧 Features

- 🖱️ Mouse control using index finger movement
- 📜 Scroll control using index + middle finger gestures
- 🗣️ Voice command support using `speech_recognition`
- 🔊 Volume control using hand distance (using `pycaw`)
- 🌞 Brightness control with gestures
- 📦 GUI using `tkinter` for launching utilities
- 🎮 Supports multi-threaded gesture + voice execution

---

## 🚀 Tech Stack

- `Python`
- `OpenCV`
- `Mediapipe`
- `Pynput`, `PyAutoGUI`
- `SpeechRecognition` + `pyttsx3`
- `screen-brightness-control`, `pycaw`
- `Tkinter` for GUI

---

## 📦 Installation

### 1. Clone the repository

git clone https://github.com/yourusername/intuitive-control-system.git
cd intuitive-control-system


### 2. Create a virtual environment (optional but recommended)
python -m venv env
env\Scripts\activate  # Windows
# OR
source env/bin/activate  # Mac/Linux

pip install opencv-python mediapipe numpy pyautogui pynput screeninfo screen-brightness-control speechrecognition pyttsx3 comtypes pycaw


## How to Run
python main.py
Make sure your webcam is connected. Press q in the video window to exit.

## Gesture/Action	Function
Index Finger	Move mouse
Index + Thumb Touch	Left Click
Thumb + Pinky	Right Click
Index + Middle Upwards	Scroll Down
Index + Middle Down	Scroll Up
Distance between Thumb & Index	Volume Control
Palm Up	Increase Brightness
Palm Down	Decrease Brightness
GUI Buttons	Open Apps / Utilities

## Project Structure
bash
Copy
Edit
├── main.py
├── gesture_module.py
├── voice_control.py
├── gui_launcher.py
├── README.md
└── requirements.txt

