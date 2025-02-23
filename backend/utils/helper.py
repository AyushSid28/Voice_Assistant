import openai
import webbrowser
import datetime
import os
import json
import pyttsx3
import threading
import queue
import time
from backend.config.config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

engine = pyttsx3.init()
speech_queue = queue.Queue()
speech_running = threading.Event()
listening = True  

def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break  

        if speech_running.is_set():
            time.sleep(0.1)  
        
        speech_running.set()
        print(f"Speaking: {text}")

        engine.say(text)
        engine.runAndWait()  
        
        speech_running.clear()
        speech_queue.task_done()

speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

def speak(text):
    speech_queue.put(text)

def get_time():
    now = datetime.datetime.now()
    response = now.strftime("The current time is %I:%M %p.")
    speak(response)
    return response

#Automated the process for opening website when Anyone says to open them
def open_website(site_name):
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "github": "https://github.com"
    }
    
    if site_name in websites:
        webbrowser.open(websites[site_name])
        response = f"Opening {site_name}..."
        speak(response)
        return response
    
    error_message = "Sorry, I don't have that website in my database."
    speak(error_message)
    return error_message

def set_reminder(task):
    reminders_file = "reminders.json"

    if os.path.exists(reminders_file):
        with open(reminders_file, "r") as file:
            reminders = json.load(file)
    else:
        reminders = []

    reminders.append(task)
    
    with open(reminders_file, "w") as file:
        json.dump(reminders, file)

    response = f"Reminder set: {task}"
    speak(response)
    return response

def get_reminders():
    reminders_file = "reminders.json"

    if os.path.exists(reminders_file):
        with open(reminders_file, "r") as file:
            reminders = json.load(file)
        response = "Here are your reminders: " + ", ".join(reminders)
        speak(response)
        return response
    
    error_message = "You have no reminders."
    speak(error_message)
    return error_message

#Here we will process the user input  and listen closely for Stop and Wake Up
def process_text(user_input):
    global listening 

    user_input = user_input.lower()

    if "stop" in user_input:
        listening = False
        response = "Evoke me when you need help!"
        print(response)
        speak(response)
        return response

    elif "wake up" in user_input:
        listening = True
        response = "I am awake! How can I assist you?"
        print(response)
        speak(response)
        return response

    elif "time" in user_input:
        return get_time()

    elif "open" in user_input:
        site_name = user_input.split("open")[-1].strip()
        return open_website(site_name)

    elif "set reminder" in user_input:
        task = user_input.replace("set reminder", "").strip()
        return set_reminder(task)

    elif "reminders" in user_input:
        return get_reminders()

    else:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        ).choices[0].message.content

        speak(response)
        return response
