import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import threading
import tkinter as tk
from tkinter import scrolledtext
import math
import winsound
import ctypes

# ---------------------- TTS ENGINE --------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 185)

def speak(text):
    console_insert(f"Assistant: {text}\n")
    engine.say(text)
    engine.runAndWait()

def speak_async(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()

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
ACCENT = "#00bbff"
CARD = "#1e1e1e"
BTN = "#2c2c2c"

root.configure(bg=BG)

# ---------- TITLE ----------
tk.Label(root, text="🎙️ Modern Voice Assistant",
         font=("Segoe UI", 20, "bold"),
         bg=CARD, fg=ACCENT, pady=10).pack(fill="x")

# ---------- STATUS ----------
status_label = tk.Label(root, text="Status: Idle",
                        font=("Segoe UI", 12, "bold"),
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
canvas.pack(pady=20)

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
    speak_async("Locking system")
    ctypes.windll.user32.LockWorkStation()

# ---------------------- SPEECH ------------------------------
def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source, timeout=4, phrase_time_limit=5)

        cmd = r.recognize_google(audio, language="en-in").lower()
        console_insert(f"You: {cmd}\n")
        return cmd
    except:
        return ""

def clean_text(cmd):
    fillers = [
        "hey assistant", "assistant", "please",
        "can you", "tell me", "what is", "current", "now"
    ]
    for f in fillers:
        cmd = cmd.replace(f, "")
    return cmd.strip()

def process_voice():
    speak_async("Assistant ready")

    while listening:
        cmd = clean_text(take_command())

        if not cmd:
            continue

        # -------- TIME --------
        if "time" in cmd or "clock" in cmd:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak_async(f"The current time is {time_now}")

        # -------- YOUTUBE --------
        elif "youtube" in cmd:
            speak_async("Opening YouTube")
            webbrowser.open("https://youtube.com")

        # -------- GOOGLE SEARCH --------
        elif "search" in cmd:
            query = cmd.replace("search", "").strip()
            if query:
                speak_async(f"Searching Google for {query}")
                webbrowser.open(
                    f"https://www.google.com/search?q={query.replace(' ', '+')}"
                )

        # -------- VOLUME --------
        elif "increase volume" in cmd or "volume up" in cmd:
            volume_up()
            speak_async("Volume increased")

        elif "decrease volume" in cmd or "volume down" in cmd:
            volume_down()
            speak_async("Volume decreased")

        elif "mute" in cmd:
            volume_mute()
            speak_async("Volume muted")

        # -------- SYSTEM --------
        elif "lock" in cmd:
            lock_system()

        elif "stop assistant" in cmd or "stop listening" in cmd:
            speak_async("Stopping assistant")
            stop_listening()

        else:
            speak_async("I did not understand")

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
console_insert("Ready. Speak any command\n")
root.mainloop()
