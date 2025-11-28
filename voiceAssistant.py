import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia

# initialize speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language="en-in")
        print("You said:", command)
        return command.lower()
    except:
        speak("I couldn't understand. Say that again.")
        return ""

def handle_command(cmd):

    if "hello" in cmd:
        speak("Hello, how can I help you?")
    
    elif "your name" in cmd:
        speak("I'm your assistant. You still haven't named me.")
    
    elif "time" in cmd:
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {time}")

    elif "date" in cmd:
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")

    elif "search" in cmd:
        speak("What should I search?")
        query = listen()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")

    elif "open youtube" in cmd:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in cmd:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "wikipedia" in cmd:
        speak("What should I search on Wikipedia?")
        topic = listen()
        if topic:
            result = wikipedia.summary(topic, sentences=2)
            print(result)
            speak(result)

    elif "stop" in cmd or "exit" in cmd:
        speak("Goodbye.")
        exit()

    else:
        speak("I didn't understand. Try again.")

def start():
    speak("Voice assistant activated.")
    while True:
        cmd = listen()
        if cmd:
            handle_command(cmd)

start()
