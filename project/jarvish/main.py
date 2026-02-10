import speech_recognition as sr
import datetime
import os
import subprocess
import webbrowser


# ================= REAL TTS (WINDOWS SAPI) =================


def speak(text):
    print("JARVIS:", text)
    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Speak("{text}");
    '''
    subprocess.run(["powershell", "-Command", command], capture_output=True)

# ================= VOICE INPUT =================


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I am listening")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        speak("Processing your command")
        query = r.recognize_google(audio, language="en-in")
        print("USER:", query)
        return query.lower()

    except:
        speak("Sorry, I did not understand")
        return ""


# ================= START =================
speak("Hello, I am Jarvis. System is fully ready.")

# ================= MAIN LOOP =================
while True:
    command = take_command()

    if command == "":
        continue

    if "time" in command:
        speak("Checking time")
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + time_now)

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open chrome" in command:
        speak("Opening Google Chrome")
        os.system("start chrome")

    elif "open vscode" in command or "open vs code" in command:
        speak("Opening Visual Studio Code")
        os.system("code")

    elif "open file" in command or "open file explorer" in command:
        speak("Opening File Explorer")
        os.system("explorer")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "search google" in command:
        speak("Searching on Google")
        query = command.replace("search google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "play youtube" in command:
        speak("Playing on YouTube")
        query = command.replace("play youtube", "").strip()
        webbrowser.open(
            f"https://www.youtube.com/results?search_query={query}")

    elif "exit" in command or "stop" in command:
        speak("Shutting down. Goodbye.")
        break

    else:
        speak("This command is not programmed yet")
