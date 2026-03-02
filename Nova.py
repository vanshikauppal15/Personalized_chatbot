
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
from groq import Groq
from config import apikey, weather_api_key

chat_history = [
    {"role": "system", "content": "You are Nova, a smart, friendly desktop AI assistant created by Vanshika. Speak concisely and helpfully."}
]
chat_mode = False

def chat(user_query):
    global chat_history

    try:
        client = Groq(api_key=apikey)

        print("\nNova is thinking...")

        # Add user message
        chat_history.append({"role": "user", "content": user_query})


        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=chat_history,
            temperature=0.7
        )

        output = response.choices[0].message.content

        # Add AI response to history
        chat_history.append({"role": "assistant", "content": output})

        print(f"Nova: {output}")

        say(output)

    except Exception as e:
        print("Error:", e)
        say("Sorry, something went wrong with AI.")
# ================= TEXT TO SPEECH =================
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()


# ================= AI FUNCTION =================
def ai(prompt):
    try:
        client = Groq(api_key=apikey)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content

        print("\n AI says:\n")
        print(output)

        say(output)

    except Exception as e:
        print("Error:", e)
        say("Sorry, something went wrong with AI.")

# ================= WEATHER FUNCTION =================
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if str(data.get("cod")) != "200":
            return "Sorry, I couldn't find that city."

        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        report = (
            f"Weather in {city}:\n"
            f"Temperature: {temperature} degree Celsius.\n"
            f"Condition: {description}.\n"
            f"Humidity: {humidity} percent."
        )

        # Smart Advice
        if temperature > 35:
            report += "\nIt is very hot. Stay hydrated."
        elif temperature < 10:
            report += "\nIt is cold. Wear warm clothes."
        else:
            report += "\nWeather looks pleasant."

        return report

    except requests.exceptions.RequestException as e:
        return "Sorry, I couldn't fetch the weather."


# ================= VOICE INPUT =================
def take_voice_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"\n You said: {query}\n")
        say(f"You said {query}")
        return query

    except sr.UnknownValueError:
        print("Could not understand the audio.")
        say("Sorry, I didn't understand that.")
        return None

    except sr.RequestError as e:
        print(f"Request failed; {e}")
        say("Sorry, there was a network error.")
        return None


# ================= MAIN PROGRAM =================
if __name__ == '__main__':

    say("Hello, I am Nova. How can I help you?")
    print(" Nova is ready...")

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"]
    ]

    apps = [
        ["vs code", r"C:\Users\rishu\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"],
        ["word", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010.lnk"],
        ["powerpoint", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"],
        ["excel", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"]
    ]

    while True:
        print("\nPress Enter to speak or type your command directly:")
        typed = input("Your command (leave empty to use voice): ")

        if typed.strip() == "":
            query = takeVoiceCommand()
            if query is None:
                continue
        else:
            query = typed
            print(f"You typed: {query}")
            say(f"You typed {query}")

        query = query.lower()

        # ===== OPEN WEBSITES =====
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} now...")
                webbrowser.open(site[1])
                break

        # ===== PLAY MUSIC =====
        if "play music" in query or "open music" in query:
            say("Playing music of your choice")

            search_query = query.replace("play music", "").replace("open music", "").strip()

            if search_query == "":
                search_query = "latest songs"

            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        # ===== TIME =====
        if "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strfTime}")

        # ===== OPEN APPS =====
        for app in apps:
            if f"open {app[0]}" in query:
                say(f"Opening {app[0]} now...")
                webbrowser.open(app[1])
                break

        # ===== WEATHER =====
        if "weather" in query:
            say("Which city?")
            print("Which city?")

            city_input = input("Enter city name: ")

            if city_input.strip() == "":
                city = takeVoiceCommand()
            else:
                city = city_input
            if city is None:
                say("Sorry, I didn't catch that.")
                continue

            else:
                weather_report = get_weather(city)
                print(weather_report)
                say(weather_report)

        # ===== AI SINGLE QUESTION =====
        if query.startswith("ask ai"):
            clean_prompt = query.replace("ask ai", "").strip()
            if clean_prompt == "":
                say("What should I ask the AI?")
            else:
                ai(prompt=clean_prompt)

        # ===== CONTINUOUS CHAT MODE =====
        # ===== START CHAT MODE =====
        if query == "start chat":
            chat_mode = True
            say("Chat mode activated.")
            print(" Chat mode ON")
            continue

        # ===== EXIT CHAT MODE =====
        if query == "exit chat":
            chat_mode = False
            say("Exiting chat mode.")
            print("Chat mode OFF")
            continue

        # ===== CONTINUOUS CHAT =====
        if chat_mode:
            print(f"Vanshika: {query}")
            chat(query)
            continue

        # ===== RESET CHAT =====
        elif "reset chat" in query:
            chat_history.clear()
            say("Chat history has been reset.")
            print("Chat history cleared.")

        # ===== EXIT =====
        elif "nova quit" in query:
            say("Shutting down. Goodbye Vanshika.")
            break




