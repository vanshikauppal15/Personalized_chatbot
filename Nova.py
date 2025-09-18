import speech_recognition as sr
import pyaudio
import pyttsx3
import os
import webbrowser

print("PyAudio version:", pyaudio.__version__)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeVoiceCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        r.pause_threshold = 1.2
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')

        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Request failed; {e}")
        return None

if __name__ == '__main__':
    print('PyCharm')
    say("Hello I am Nova")

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"]
    ]

    while True:
        print("\nPress Enter to use voice command or type your command directly:")
        typed = input("Your command (leave empty to use voice): ")

        if typed.strip() == "":
            query = takeVoiceCommand()
            if query is None:
                say("Sorry, I couldn't hear you.")
                continue
        else:
            query = typed
            say(f"You typed {query}")

        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break


