import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import subprocess
import time
import threading
import tkinter as tk
from tkinter import scrolledtext

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# GUI Window
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("600x400")
root.configure(bg="#222222")

# Log Box
log_box = scrolledtext.ScrolledText(root, width=70, height=20, bg="#1e1e1e", fg="white", font=("Consolas", 10))
log_box.pack(pady=10)

def gui_log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)

def speak(text):
    gui_log(f"🤖: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        gui_log(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, the speech service is down.")
        return ""

def process_command(command):
    if "open chrome" in command:
        speak("Opening Google Chrome")
        os.system("start chrome")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open chat gpt" in command or "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com/")

    elif "open gmail" in command or "open g mail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com/")

    elif "open my computer" in command or "open this pc" in command:
        speak("Opening This PC")
        os.system("explorer shell:MyComputerFolder")

    elif "open documents folder" in command or "open my documents" in command:
        speak("Opening Documents folder")
        os.system("explorer shell:Personal")

    elif "open c drive" in command:
        speak("Opening C drive")
        os.system("explorer C:\\")

    elif "open d drive" in command:
        speak("Opening D drive")
        os.system("explorer D:\\")

    elif "open e drive" in command:
        speak("Opening E drive")
        os.system("explorer E:\\")

    elif "open downloads folder" in command:
        speak("Opening Downloads folder")
        downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
        os.system(f"explorer {downloads_path}")

    elif "open desktop" in command:
        speak("Opening Desktop folder")
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        os.system(f"explorer {desktop_path}")

    elif "open pictures" in command:
        speak("Opening Pictures folder")
        pictures_path = os.path.join(os.environ["USERPROFILE"], "Pictures")
        os.system(f"explorer {pictures_path}")

    elif "open recycle bin" in command:
        speak("Opening Recycle Bin")
        subprocess.run('explorer.exe shell:RecycleBinFolder', shell=True)


    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("start notepad")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("start calc")

    elif "open word" in command:
        speak("Opening Microsoft Word")
        os.system("start winword")

    elif "open excel" in command:
        speak("Opening Microsoft Excel")
        os.system("start excel")

    elif "open powerpoint" in command:
        speak("Opening Microsoft PowerPoint")
        os.system("start powerpnt")

    elif "open paint" in command:
        speak("Opening Paint")
        os.system("start mspaint")

    elif "open file explorer" in command or "open explorer" in command:
        speak("Opening File Explorer")
        os.system("start explorer")

    elif "open cmd" in command or "open command prompt" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "open control panel" in command:
        speak("Opening Control Panel")
        os.system("control")

    elif "open task manager" in command:
        speak("Opening Task Manager")
        os.system("start taskmgr")

    elif "open settings" in command:
        speak("Opening Windows Settings")
        os.system("start ms-settings:")

    elif "shutdown" in command:
        speak("Shutting down in 5 seconds")
        time.sleep(5)
        os.system("shutdown /s /t 1")

    elif "restart" in command:
        speak("Restarting in 5 seconds")
        time.sleep(5)
        os.system("shutdown /r /t 1")

    elif "exit" in command or "close" in command:
        speak("Goodbye!")
        root.quit()

    else:
        speak("Sorry, I don't recognize that command.")

def run_assistant():
    while running_flag[0]:
        cmd = listen_command()
        if cmd:
            process_command(cmd)

def start_assistant():
    if not running_flag[0]:
        running_flag[0] = True
        threading.Thread(target=run_assistant, daemon=True).start()
        gui_log("🎤 Voice Assistant Started")

def stop_assistant():
    running_flag[0] = False
    gui_log("⛔ Voice Assistant Stopped")

# Buttons
button_frame = tk.Frame(root, bg="#222222")
button_frame.pack(pady=5)

start_button = tk.Button(button_frame, text="Start", command=start_assistant, bg="#4CAF50", fg="white", width=15)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_assistant, bg="#f44336", fg="white", width=15)
stop_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=root.quit, bg="#607D8B", fg="white", width=15)
exit_button.grid(row=0, column=2, padx=10)

# Flags
running_flag = [False]

# Start GUI
speak("Voice Control System ready.")
root.mainloop()
