import sys
import os
import streamlit as st
import speech_recognition as sr
import pyttsx3  


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.helper import process_text  


st.title("Voice Assistant AI")


recognizer = sr.Recognizer()


mic_list = sr.Microphone.list_microphone_names()
st.write("Available Microphones:", mic_list)


mic = sr.Microphone(device_index=0)

#Convert Speech to Text

def speak(text):
   
    engine = pyttsx3.init()  
    engine.setProperty('rate', 150)  
    engine.setProperty('volume', 1)  
    engine.say(text)
    engine.runAndWait()  

def listen_for_wake_word():
   
    with mic as source:
        st.write("Listening for 'Ayush' to activate...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None


#Get the User Question after assistant activation
def get_voice_input():
    
    with mic as source:
        st.write("Listening for your question...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=10)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Speech Recognition API is not available."

def assistant_process():
    
    command = listen_for_wake_word()
    
    if command and "ayush" in command:
        st.success("Assistant Activated! How can I help?")
        user_input = get_voice_input()
        response = process_text(user_input)
        
        st.write(f"Response: {response}")
        speak(response)  
    else:
        st.error("Didn't hear 'Ayush'. Please try again.")

#Activate the assistant Button
if st.button("Activate Assistant (Say 'Ayush')"):
    assistant_process()
