import tkinter as tk
from tkinter import messagebox
import subprocess
import platform
import pyautogui

def run_script(script_name):
    subprocess.Popen(["python", script_name], shell=True)

# Main window
app = tk.Tk()
app.title("💡 Intuitive Control System")
app.geometry("600x650")
app.configure(bg="#1a1a1a")

# Styles
TITLE_FONT = ("Helvetica", 22, "bold")
SUBTITLE_FONT = ("Helvetica", 14)
BUTTON_FONT = ("Helvetica", 13)
BUTTON_BG = "#292929"
BUTTON_FG = "#00ffcc"
BUTTON_HOVER_BG = "#00ffcc"
BUTTON_HOVER_FG = "#1a1a1a"

# Hover effects
def on_enter(e):
    e.widget["background"] = BUTTON_HOVER_BG
    e.widget["foreground"] = BUTTON_HOVER_FG

def on_leave(e):
    e.widget["background"] = BUTTON_BG
    e.widget["foreground"] = BUTTON_FG

# Title
tk.Label(
    app,
    text="💡 Intuitive Control System",
    font=TITLE_FONT,
    bg="#1a1a1a",
    fg="#00ffcc"
).pack(pady=25)

# Subtitle
tk.Label(
    app,
    text="Select a Control Function",
    font=SUBTITLE_FONT,
    bg="#1a1a1a",
    fg="white"
).pack(pady=5)

# Create button
def create_button(label, script=None, command=None):
    btn = tk.Button(
        app,
        text=label,
        font=BUTTON_FONT,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        activebackground=BUTTON_HOVER_BG,
        activeforeground=BUTTON_HOVER_FG,
        width=36,
        height=2,
        border=0,
        command=command if command else lambda: run_script(script)
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=8)
    return btn

# App buttons
create_button("🖱️Mouse Control", "mouse_control.py")
create_button("💡  Brightness Control", "brightness_control.py")
create_button("🔊  Volume Control", "volume_control.py")
create_button("🎤  Speech Writer", "Speech_writer.py")
create_button("🎙️Voice Control", "voicecontrol.py")

# Additional Functionalities
def show_info():
    screen_w, screen_h = pyautogui.size()
    os_name = platform.system()
    messagebox.showinfo(
        "System Info",
        f"🖥️ Screen Resolution: {screen_w}x{screen_h}\n🧠 OS: {os_name}"
    )

def show_about():
    messagebox.showinfo(
        "About",
        "📘 Intuitive Control System\n\nControl your PC using gestures and voice."
    )

# Extra Buttons
create_button("🔍  System Info", command=show_info)
create_button("ℹ️  About", command=show_about)

# Exit Button
exit_btn = tk.Button(
    app,
    text="Exit",
    font=("Helvetica", 13, "bold"),
    bg="#ff4444",
    fg="white",
    activebackground="#ff6666",
    activeforeground="white",
    width=20,
    height=2,
    command=app.quit
)
exit_btn.pack(pady=30)

app.mainloop()
