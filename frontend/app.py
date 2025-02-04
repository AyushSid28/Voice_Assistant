import sys
import os
import streamlit as st
import speech_recognition as sr
import pyttsx3  


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.helper import process_text  

st.title("🎤 Voice Assistant AI")


recognizer = sr.Recognizer()


mic_list = sr.Microphone.list_microphone_names()
st.write("Available Microphones:", mic_list)


mic = sr.Microphone(device_index=0)

def speak(text):
    """Convert text to speech with a fresh instance of pyttsx3."""
    engine = pyttsx3.init()  
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()  

def listen_for_hey_john():
    """Listen for the wake word 'John'."""
    with mic as source:
        st.write("🎤 Listening for 'John'...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def get_voice_input():
    """Listen for user's question."""
    with mic as source:
        st.write("🗣️ Listening for your question...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=10)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Speech Recognition API is not available."

def assistant_process():
    """Handles assistant activation inline (without threading)."""
    command = listen_for_hey_john()
    
    if command and "john" in command:
        st.success("✅ Assistant Activated! Listening...")
        user_input = get_voice_input()
        response = process_text(user_input)
        
        st.write(f"**AI Response:** {response}")
        speak(response)  
    else:
        st.error("❌ Didn't hear 'John'. Try again.")


if st.button("Activate Assistant (Say 'John')"):
    assistant_process()
