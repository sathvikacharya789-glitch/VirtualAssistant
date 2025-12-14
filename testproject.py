import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import threading
import tkinter as tk
from tkinter import scrolledtext
import math
import winsound
import os
import ctypes

# ---------------------- TTS ENGINE --------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak(text):
    console_insert(f"Assistant: {text}\n")
    engine.say(text)
    engine.runAndWait()

# ---------------------- BEEP SOUNDS -------------------------
def beep_start():
    winsound.Beep(1200, 150)

def beep_stop():
    winsound.Beep(600, 150)

# ---------------------- GUI SETUP ---------------------------
root = tk.Tk()
root.title("Modern Voice Assistant")
root.state("zoomed")

BG = "#121212"
FG = "#ffffff"
ACCENT = "#00eaff"
CARD = "#1e1e1e"
BTN = "#2c2c2c"

root.configure(bg=BG)

# ---------- TITLE ----------
title = tk.Label(root, text="🎙️ Modern Voice Assistant",
                 font=("Segoe UI", 20, "bold"),
                 bg=CARD, fg=ACCENT, pady=10)
title.pack(fill="x")

# ---------- STATUS ----------
status_label = tk.Label(root, text="Status: Idle",
                        font=("Segoe UI", 12),
                        bg=BG, fg=FG)
status_label.pack(pady=5)

# ---------- CONSOLE ----------
console_frame = tk.Frame(root, bg=CARD)
console_frame.pack(padx=15, pady=10, fill="x")

console = scrolledtext.ScrolledText(
    console_frame, height=18,
    bg="#101010", fg="#00ffcc",
    font=("Consolas", 11), bd=0
)
console.pack(padx=8, pady=8, fill="x")

def console_insert(text):
    console.insert(tk.END, text)
    console.yview(tk.END)

# ---------- MIC ANIMATION ----------
canvas = tk.Canvas(root, width=180, height=180,
                   bg=BG, highlightthickness=0)
canvas.pack(pady=10)

circle = canvas.create_oval(60, 60, 120, 120,
                            outline=ACCENT, width=3)
ring = canvas.create_oval(40, 40, 140, 140,
                          outline=ACCENT, width=2)

pulse_angle = 0
listening = False

def animate_pulse():
    global pulse_angle
    if not listening:
        canvas.coords(circle, 60, 60, 120, 120)
        canvas.coords(ring, 50, 50, 130, 130)
        return

    pulse_angle += 0.2
    s = 8 * math.sin(pulse_angle)

    canvas.coords(circle, 60-s, 60-s, 120+s, 120+s)
    canvas.coords(ring, 40-2*s, 40-2*s, 140+2*s, 140+2*s)

    root.after(40, animate_pulse)

# ---------------------- SYSTEM CONTROL ----------------------
def volume_up():
    for _ in range(5):
        ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)

def volume_down():
    for _ in range(5):
        ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)

def volume_mute():
    ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)

def lock_system():
    speak("Locking system")
    ctypes.windll.user32.LockWorkStation()

# ---------------------- SPEECH ------------------------------
def take_command():
    r = sr.Recognizer()
    r.pause_threshold = 0.8
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source)

        cmd = r.recognize_google(audio, language="en-in").lower()
        console_insert(f"You: {cmd}\n")
        return cmd
    except:
        return ""

def process_voice():
    speak("Assistant ready. Say hey assistant.")

    while listening:
        cmd = take_command()

        if "hey assistant" not in cmd:
            continue

        speak("Yes?")
        cmd = take_command()

        if "time" in cmd:
            speak(datetime.datetime.now().strftime("The time is %I:%M %p"))

        elif "open youtube" in cmd:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "increase volume" in cmd:
            volume_up()
            speak("Volume increased")

        elif "decrease volume" in cmd:
            volume_down()
            speak("Volume decreased")

        elif "mute volume" in cmd:
            volume_mute()
            speak("Volume muted")

        elif "lock system" in cmd:
            lock_system()


        elif "stop assistant" in cmd:
            speak("Stopping assistant")
            stop_listening()

        else:
            speak("I did not understand")

# ---------------------- CONTROLS ----------------------------
def start_listening():
    global listening
    if not listening:
        listening = True
        status_label.config(text="Status: Listening")
        beep_start()
        animate_pulse()
        threading.Thread(target=process_voice, daemon=True).start()

def stop_listening():
    global listening
    listening = False
    status_label.config(text="Status: Idle")
    beep_stop()

# ---------------------- BUTTONS -----------------------------
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🎤 Start",
          width=20, font=("Segoe UI", 12, "bold"),
          bg=BTN, fg=FG, command=start_listening).grid(row=0, column=0, padx=15)

tk.Button(btn_frame, text="⏹ Stop",
          width=20, font=("Segoe UI", 12, "bold"),
          bg=BTN, fg=FG, command=stop_listening).grid(row=0, column=1, padx=15)

# ---------------------- RUN -------------------------------
console_insert("Ready. Say 'Hey Assistant'\n")
root.mainloop()
