import openai
import webbrowser
import datetime
import os
import json
import requests
import pyttsx3
import threading
import queue
import time
from bs4 import BeautifulSoup
from backend.config.config import OPENAI_API_KEY

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize text-to-speech engine
engine = pyttsx3.init()
speech_queue = queue.Queue()
speech_running = threading.Event()  # Flag to track speech state


def speech_worker():
    """ Continuously processes speech queue to avoid overlapping speech """
    while True:
        text = speech_queue.get()
        if text is None:
            break  # Exit loop if None is received

        if speech_running.is_set():
            time.sleep(0.1)  # Wait if speech is already running
        
        speech_running.set()
        print(f"Speaking: {text}")  # Debug print
        
        # ✅ FIX: Create a new pyttsx3 instance every time to avoid threading issues
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        
        speech_running.clear()
        speech_queue.task_done()

# Start speech thread
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

def speak(text):
    """ Adds text to speech queue for processing """
    speech_queue.put(text)

# Function to get the current time
def get_time():
    now = datetime.datetime.now()
    response = now.strftime("The current time is %I:%M %p.")
    speak(response)
    return response

# Function to fetch weather data
def get_weather(city="New Delhi"):
    api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if "main" in response:
        temperature = response["main"]["temp"]
        description = response["weather"][0]["description"]
        weather_info = f"The temperature in {city} is {temperature}°C with {description}."
        speak(weather_info)
        return weather_info
    
    error_message = "Sorry, I couldn't fetch the weather data."
    speak(error_message)
    return error_message

# Function to open websites
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

# Function to play YouTube videos
def play_youtube(query):
    """Search YouTube and play the first available video."""
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find first video link
    video_links = soup.find_all("a", href=True)
    for link in video_links:
        if "/watch?" in link["href"]:
            video_url = f"https://www.youtube.com{link['href']}"
            webbrowser.open(video_url)
            response = f"Playing {query} on YouTube."
            speak(response)
            return response

    error_message = "Sorry, I couldn't find a video for that."
    speak(error_message)
    return error_message

# Function to set reminders
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

# Function to fetch reminders
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

# Function to fetch top news headlines
def get_news():
    api_key = "YOUR_NEWSAPI_KEY"  # Replace with your News API key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url).json()

    if "articles" in response:
        headlines = [article["title"] for article in response["articles"][:5]]
        news_response = "Here are the top news headlines: " + "; ".join(headlines)
        speak(news_response)
        return news_response
    
    error_message = "Sorry, I couldn't fetch news at the moment."
    speak(error_message)
    return error_message

# Main process function
def process_text(user_input):
    user_input = user_input.lower()

    if "time" in user_input:
        return get_time()
    
    elif "weather" in user_input:
        city = user_input.split("weather in")[-1].strip() if "weather in" in user_input else "New Delhi"
        return get_weather(city)
    
    elif "open" in user_input:
        site_name = user_input.split("open")[-1].strip()
        return open_website(site_name)
    
    elif "play" in user_input and "on youtube" in user_input:
        query = user_input.replace("play", "").replace("on youtube", "").strip()
        return play_youtube(query)

    elif "set reminder" in user_input:
        task = user_input.replace("set reminder", "").strip()
        return set_reminder(task)

    elif "reminders" in user_input:
        return get_reminders()

    elif "news" in user_input:
        return get_news()

    else:
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        ).choices[0].message.content

        speak(response)
        return response
