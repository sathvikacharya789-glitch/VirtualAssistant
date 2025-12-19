import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import threading
import tkinter as tk
import os
from tkinter import scrolledtext
import math

# ---------------------- TTS ENGINE --------------------------
try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
except:
    engine = None

def speak(text):
    console_insert(f"Assistant: {text}\n")
    if engine:
        engine.say(text)
        engine.runAndWait()

# ---------------------- GUI SETUP ---------------------------
root = tk.Tk()
root.title("Voice Assistant")
root.state("zoomed")

# ---------- THEMES ----------
DARK = {
    "BG": "#121212", "CARD": "#1e1e1e", "FG": "#ffffff",
    "ACCENT": "#00eaff", "BTN": "#2c2c2c"
}
LIGHT = {
    "BG": "#f5f5f5", "CARD": "#ffffff", "FG": "#000000",
    "ACCENT": "#0078ff", "BTN": "#dddddd"
}
theme = DARK

def apply_theme():
    root.configure(bg=theme["BG"])
    title_frame.config(bg=theme["CARD"])
    title_label.config(bg=theme["CARD"], fg=theme["ACCENT"])
    status_label.config(bg=theme["BG"], fg=theme["FG"])
    console_frame.config(bg=theme["CARD"])
    console.config(bg=theme["BG"], fg=theme["ACCENT"])
    pulse_canvas.config(bg=theme["BG"])
    for b in buttons:
        b.config(bg=theme["BTN"], fg=theme["FG"])

def toggle_theme():
    global theme
    theme = LIGHT if theme == DARK else DARK
    apply_theme()

# ---------- Title ----------
title_frame = tk.Frame(root, pady=10)
title_frame.pack(fill="x")

title_label = tk.Label(
    title_frame, text="🎙️ Modern Voice Assistant",
    font=("Segoe UI", 20, "bold")
)
title_label.pack()

# ---------- Status ----------
status_label = tk.Label(root, text="Status: Idle", font=("Segoe UI", 12))
status_label.pack(pady=5)

# ---------- Console ----------
console_frame = tk.Frame(root, bd=2)
console_frame.pack(pady=10, padx=15, fill="x")

console = scrolledtext.ScrolledText(
    console_frame, wrap=tk.WORD, height=20,
    font=("Consolas", 11), bd=0
)
console.pack(padx=8, pady=8, fill="x")

def console_insert(text):
    console.insert(tk.END, text)
    console.yview(tk.END)

# ---------- Mic Animation ----------
pulse_canvas = tk.Canvas(root, width=180, height=180, highlightthickness=0)
pulse_canvas.pack(pady=10)

circle = pulse_canvas.create_oval(60, 60, 120, 120, width=3)
ring = pulse_canvas.create_oval(40, 40, 140, 140, width=2)

listening = False
pulse_angle = 0

def animate_pulse():
    global pulse_angle
    if not listening:
        pulse_canvas.itemconfig(circle, outline=theme["ACCENT"])
        pulse_canvas.coords(circle, 60, 60, 120, 120)
        pulse_canvas.coords(ring, 50, 50, 130, 130)
        return

    pulse_angle += 0.2
    s = 8 * math.sin(pulse_angle)

    pulse_canvas.coords(circle, 60-s, 60-s, 120+s, 120+s)
    pulse_canvas.coords(ring, 40-2*s, 40-2*s, 140+2*s, 140+2*s)
    pulse_canvas.itemconfig(circle, outline=theme["ACCENT"])
    pulse_canvas.itemconfig(ring, outline=theme["ACCENT"])

    root.after(40, animate_pulse)

# ---------------------- CORE --------------------------
def get_time():
    speak("The time is " + datetime.datetime.now().strftime("%I:%M %p"))

def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://youtube.com")

def web_search(q):
    speak(f"Searching for {q}")
    webbrowser.open(f"https://google.com/search?q={q}")

# ---------------------- SPEECH --------------------------
def take_command():
    r = sr.Recognizer()
    r.pause_threshold = 0.8

    try:
        with sr.Microphone() as src:
            r.adjust_for_ambient_noise(src, duration=0.2)
            audio = r.listen(src)

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
            get_time()
        elif "youtube" in cmd:
            open_youtube()
        elif "search" in cmd:
            web_search(cmd.replace("search", ""))
        elif "stop" in cmd:
            speak("Stopping assistant")
            stop_listening()
        else:
            speak("I didn't understand")

# ---------------------- CONTROLS --------------------------
def start_listening():
    global listening
    if not listening:
        listening = True
        status_label.config(text="Status: Listening")
        animate_pulse()
        threading.Thread(target=process_voice, daemon=True).start()

def stop_listening():
    global listening
    listening = False
    status_label.config(text="Status: Idle")

def clear_console():
    console.delete("1.0", tk.END)

# ---------- Buttons ----------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

buttons = []

def add_btn(text, cmd):
    b = tk.Button(btn_frame, text=text, width=20, pady=10,
                  font=("Segoe UI", 11, "bold"), command=cmd)
    b.pack(side="left", padx=10)
    buttons.append(b)

add_btn("🎤 Start", start_listening)
add_btn("⏹ Stop", stop_listening)
add_btn("🧹 Clear Console", clear_console)
add_btn("🌗 Toggle Theme", toggle_theme)

apply_theme()
console_insert("Ready. Say 'Hey Assistant'\n")
root.mainloop()
