import datetime
import webbrowser
import os
import speech_recognition as sr
import pyttsx3
import threading
import tkinter as tk
from tkinter import scrolledtext


# -------------------- TTS SETUP --------------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    chat.insert(tk.END, f"Assistant: {text}\n")
    chat.see(tk.END)
    engine.say(text)
    engine.runAndWait()

# -------------------- ASSISTANT FUNCTIONS --------------------
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning. How can I help you?")
    elif hour < 18:
        speak("Good afternoon. What can I do for you?")
    else:
        speak("Good evening. How may I assist you?")

def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}")

def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def web_search(query):
    speak(f"Searching Google for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")

# -------------------- SPEECH RECOGNITION --------------------
def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            status.config(text="Listening...", fg="green")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=4, phrase_time_limit=5)

        command = r.recognize_google(audio, language="en-in").lower()
        chat.insert(tk.END, f"You: {command}\n")
        chat.see(tk.END)
        return command
    except:
        speak("Sorry, I didn't catch that.")
        return ""

# -------------------- MAIN LOGIC --------------------
def assistant_loop():
    while running:
        cmd = take_command()
        if not cmd:
            continue

        if any(word in cmd for word in ["stop", "exit", "quit", "bye"]):
            speak("Goodbye")
            stop_assistant()
            break

        elif "time" in cmd:
            get_time()

        elif "youtube" in cmd:
            open_youtube()

        elif "search" in cmd:
            query = cmd.replace("search", "").replace("for", "").strip()
            if query:
                web_search(query)
            else:
                speak("What should I search for?")

        else:
            speak("Command not recognized.")

# -------------------- CONTROL --------------------
def start_assistant():
    global running
    running = True
    threading.Thread(target=assistant_loop, daemon=True).start()

def stop_assistant():
    global running
    running = False
    status.config(text="Idle", fg="red")

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

tk.Label(root, text="VOICE ASSISTANT",
         font=("Segoe UI", 18, "bold"),
         bg="#1e1e1e", fg="#00ffff").pack(pady=10)

status = tk.Label(root, text="Idle",
                  font=("Segoe UI", 10, "bold"),
                  bg="#1e1e1e", fg="red")
status.pack()

chat = scrolledtext.ScrolledText(root, width=80, height=20,
                                 bg="#101010", fg="#00ffcc",
                                 font=("Consolas", 11))
chat.pack(padx=10, pady=10)

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="START",
          width=15, font=("Segoe UI", 11, "bold"),
          command=start_assistant).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="STOP",
          width=15, font=("Segoe UI", 11, "bold"),
          command=stop_assistant).grid(row=0, column=1, padx=10)

# -------------------- START --------------------
running = False
greet()
root.mainloop()
