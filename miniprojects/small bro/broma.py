import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# initialize
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except:
            return ""

speak("Hello, I am your Jarvis. How can I help you?")

while True:
    command = listen()
    
    if "time" in command:
        speak(f"The time is {datetime.datetime.now().strftime('%H:%M')}")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        break
