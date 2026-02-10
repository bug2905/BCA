from flask import Flask, jsonify, request
import speech_recognition as sr
import subprocess
import datetime
import os

app = Flask(__name__)


def speak(text):
    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Speak("{text}");
    '''
    subprocess.run(["powershell", "-Command", command], capture_output=True)


@app.route("/listen", methods=["GET"])
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I am listening")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-in").lower()
        response = process_command(query)
        return jsonify({"user": query, "bot": response})
    except:
        speak("Sorry, I did not understand")
        return jsonify({"user": "", "bot": "Sorry, I did not understand"})


def process_command(command):
    if "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + time_now)
        return "The time is " + time_now

    elif "open notepad" in command:
        os.system("notepad")
        speak("Opening Notepad")
        return "Opening Notepad"

    elif "open calculator" in command:
        os.system("calc")
        speak("Opening Calculator")
        return "Opening Calculator"

    elif "close calculator" in command:
        os.system("taskkill /f /im CalculatorApp.exe")
        speak("Closing Calculator")
        return "Closing Calculator"

    elif "exit" in command:
        speak("Goodbye Kushal")
        return "Goodbye Kushal"

    else:
        speak("This command is not programmed yet")
        return "This command is not programmed yet"


if __name__ == "__main__":
    app.run(debug=True)
