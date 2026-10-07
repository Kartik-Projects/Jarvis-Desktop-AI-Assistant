import os
import subprocess
import webbrowser
import urllib.parse
from datetime import datetime

import pyautogui
import speech_recognition as sr
import win32com.client
import pywhatkit
from dotenv import load_dotenv
from openai import OpenAI


# ==========================
# 1. LOAD API KEY
# ==========================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY missing. Check your .env file."
    )

client = OpenAI(api_key=api_key)


# =======================
# 2. VOICE SETUP
# =======================

speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Speech speed
speaker.Rate = 0

# Volume: 0 to 100
speaker.Volume = 100

def speak(text):
     text = str(text)
     print("JARVIS:", text)

     try:
         speaker.Speak(text)
         
     except Exception as error:
         print("Windows TTS error:", error)

# =====================
# 3. MICROPHONE SETUP
# =====================

recognizer = sr.Recognizer()


def listen():

    try:

        with sr.Microphone() as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=6,
                phrase_time_limit=10
            )

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        command = command.lower().strip()

        print("YOU:", command)

        return command

    except sr.WaitTimeoutError:

        print("Listening timeout.")
        return ""

    except sr.UnknownValueError:

        print("Could not understand the voice.")
        return ""

    except sr.RequestError as error:

        print("Speech recognition error:", error)

        speak(
            "There is a speech recognition internet error."
        )

        return ""

    except OSError as error:

        print("Microphone error:", error)

        speak(
            "I cannot access the microphone."
        )

        return ""

    except Exception as error:

        print("Listening error:", error)

        speak(
            "An error occurred while listening."
        )

        return ""


# =========================
# 4. WEBSITE LIST
# =========================

websites = {

    "youtube":
        "https://www.youtube.com",

    "google":
        "https://www.google.com",

    "facebook":
        "https://www.facebook.com",

    "linkedin":
        "https://www.linkedin.com",

    "github":
        "https://www.github.com",

    "instagram":
        "https://www.instagram.com",

    "gmail":
        "https://mail.google.com",

    "whatsapp":
        "https://web.whatsapp.com"
}


# ==============================
# 5. ALLOWED WINDOWS APPS
# ==============================

apps = {

    "notepad":
        ["notepad.exe"],

    "calculator":
        ["calc.exe"],

    "paint":
        ["mspaint.exe"]
}


# ========================
# 6. OPEN WEBSITE
# ========================

def open_website(name):

    url = websites.get(name)

    if url:

        try:

            webbrowser.open(url)

            speak(
                "Opening " + name
            )

        except Exception as error:

            print("Website error:", error)

            speak(
                "I could not open " + name
            )

    else:

        speak(
            "That website is not configured."
        )


# =========================
# 7. OPEN WINDOWS APP
# =========================

def open_app(name):

    command = apps.get(name)

    if command:

        try:

            subprocess.Popen(command)

            speak(
                "Opening " + name
            )

        except OSError as error:

            print("App error:", error)

            speak(
                "I could not open that application."
            )

    else:

        speak(
            "That application is not configured."
        )


# ===========================
# 8. PLAY YOUTUBE SONG
# ===========================

def play_song(song_name):

    song_name = song_name.strip()

    if not song_name:

        speak(
            "Please tell me the song name."
        )

        return

    speak(
        "Opening the song on YouTube."
    )

    try:

        pywhatkit.playonyt(song_name)

    except Exception as error:

        print("YouTube error:", error)

        search_url = (
            "https://www.youtube.com/results?search_query="
            + urllib.parse.quote_plus(song_name)
        )

        webbrowser.open(search_url)

        speak(
            "I could not play the song directly, "
            "so I opened the YouTube search instead."
        )


# ===========================
# 9. OPEN YOUTUBE SEARCH
# ===========================

def search_youtube(query):

    query = query.strip()

    if not query:

        speak(
            "Please tell me what you want me to search."
        )

        return

    search_url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote_plus(query)
    )

    webbrowser.open(search_url)

    speak(
        "Searching YouTube for " + query
    )


# ==========================
# 10. ASK GEMINI
# ==========================

def ask_ai(question):

    try:

        response = client.responses.create(

            model="gpt-6-luna",

            instructions=(
                    "You are JARVIS, a helpful voice assistant. "
                    "Answer clearly and briefly because your "
                    "answer will be spoken aloud. "
                    "Do not claim you performed laptop actions."
                    "unless the program actually performed them."
                ),

                input= question
            
        )

        answer = response.output_text.strip()

        if answer:

            speak(answer)

        else:

            speak(
                "I did not get a response."
            )

    except Exception as error:

        print(
            "OPENAI API error:",
            error,
            flush=True
        )

        speak(
            "I could not connect to OpenAI."
        )


# =========================
# 11. REMOVE WAKE WORD
# =========================

def clean_command(command):

    wake_words = [
        "hey jarvis",
        "hi jarvis",
        "jarvis"
    ]

    for word in wake_words:

        if command.startswith(word):

            command = (
                command[len(word):]
                .strip()
            )

            break

    return command


# ==========================
# 12. PROCESS COMMANDS
# ==========================

def process_command(command):

    if not command:

        return True

    command = clean_command(command)

    if not command:

        speak(
            "Yes, how can I help?"
        )

        return True


    # ======================
    # STOP JARVIS
    # ======================

    if command in [
        "stop",
        "stop jarvis",
        "exit",
        "exit jarvis",
        "close jarvis",
        "goodbye"
    ]:

        speak(
            "Goodbye. JARVIS is shutting down."
        )

        return False


    # ======================
    # TIME
    # ======================

    if (
         command == "time"
         or "what time is it" in command
         or "what is the time" in command
         or "tell me the time" in command
         or "current time" in command
         or "tell me current time" in command
    ):

         now = datetime.now()

         current_time = now.strftime("%I:%M %p")

         speak(
             f"The time is {current_time}"
         )

         return True

    # ======================
    # DATE
    # ======================

    if (
        command == "date"
        or "what is the date" in command
        or "today's date" in command
        or "tell me the date" in command
    ):

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )

        speak(
            "Today's date is "
            + current_date
        )

        return True


    # ======================
    # OPEN WEBSITES
    # ======================

    for name in websites:

        if (
            command == "open " + name
            or command == "launch " + name
        ):

            open_website(name)

            return True


    # ======================
    # OPEN WINDOWS APPS
    # ======================

    for name in apps:

        if (
            command == "open " + name
            or command == "launch " + name
        ):

            open_app(name)

            return True


    # ======================
    # PLAY SONG
    # ======================

    song_prefixes = [

        "play the song ",
        "play song ",
        "play "
    ]

    for prefix in song_prefixes:

        if command.startswith(prefix):

            # FIXED:
            # song_mame -> song_name

            song_name = (
                command[len(prefix):]
                .strip()
            )

            song_name = song_name.replace(
                " on youtube",
                ""
            ).strip()

            play_song(song_name)

            return True


    # ======================
    # SEARCH YOUTUBE
    # ======================

    if command.startswith(
        "search youtube for "
    ):

        query = command.replace(
            "search youtube for ",
            "",
            1
        ).strip()

        search_youtube(query)

        return True


    # ======================
    # PAUSE SONG
    # ======================

    if any(
        word in command
        for word in [
            "pause",
            "spouse",
            "stop song",
            "stop music",
            "pause song",
            "pause music"
        ]
    ):

        print(
            "Pause command detected:",
            command
        )

        try:

            pyautogui.press("k")

            speak(
                "Pausing the song."
            )

        except Exception as error:

            print(
                "Keyboard control error:",
                error
            )

            speak(
                "I could not pause the song."
            )

        return True


    # ======================
    # RESUME SONG
    # ======================

    if any(
        word in command
        for word in [
            "resume",
            "continue song",
            "continue music"
        ]
    ):

        print(
            "Resume command detected:",
            command
        )

        try:

            pyautogui.press("k")

            speak(
                "Resuming the song."
            )

        except Exception as error:

            print(
                "Keyboard control error:",
                error
            )

            speak(
                "I could not resume the song."
            )

        return True

    # ========================
    # SYSTEM VOLUME CONTROL
    # ========================

    # Increase the volume
    if any(word in command
           for word in [
               "increase volume",
               "volume up",
               "turn up the volume",
               "make it louder",
               "louder"
           ]):

            for _ in range(7):
                pyautogui.press("volumeup")

            speak("Increasing the volume.")
            return True

    # Decrease the volume
    if any(word in command
           for word in [
               "decrease volume",
               "volume down",
               "turn down the volume",
               "make it quieter",
               "quieter"
           ]):

            for _ in range(7):
                pyautogui.press("volumedown")

            speak("Decreasing the volume.")
            return True
    
    # Mute the computer   
    if any(word in command
           for word in [
               "mute",
               "mute volume",
               "mute the computer"
           ]):

            pyautogui.press("volumemute")
            speak("Muting the volume.")
            return True
    
    # Unmuting the volume
    if any(word in command
           for word in [
               "unmute",
               "unmute volume",
               "unmute the computer",
               "turn the sound back on"
           ]):

            pyautogui.press("volumemute")
            speak("Unmuting the volume.")
            return True

    # ======================
    # TAKE SCREENSHOT
    # ======================

    if any(
        phrase in command
        for phrase in [
            "take a screenshot",
            "take screenshot",
            "capture the screen",
            "capture screen",
            "screenshot"
        ]
    ):

        try:

            # Create screenshot folder
            screenshot_folder = os.path.join(
                os.path.expanduser("~"),
                "Pictures",
                "JARVIS Screenshots"
            )

            os.makedirs(
                screenshot_folder,
                exist_ok=True
            )

            # Create unique file name
            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            screenshot_path = os.path.join(
                screenshot_folder,
                f"Screenshot_{timestamp}.png"
            )

            # Take screenshot
            screenshot = pyautogui.screenshot()

            # Save screenshot
            screenshot.save(
                screenshot_path
            )

            print("Screenshot saved:",
                  screenshot_path
            )

            speak("Screenshot captured successfully.")

            return True
        
        except Exception as error:

            print("Screenshot error:", error)

            speak("I could not take the screenshot.")

            return True

    # =================================
    # AI HANDLES GENERAL QUESTIONS
    # =================================

    ask_ai(command)

    return True


# ======================
# MAIN PROGRAM
# ======================

def main():

    speak(
        "Hello! I am JARVIS."
    )

    speak(
        "How can I help you?"
    )

    running = True

    while running:

        command = listen()

        if not command:

            continue

        command = command.lower().strip()

        wake_phrases = (
            "hey jarvis",
            "hi jarvis",
            "jarvis"
        )

        # ==========================
        # WAKE WORD DETECTION
        # ==========================

        if command.startswith(
            wake_phrases
        ):

            for phrase in wake_phrases:

                if command.startswith(
                    phrase
                ):

                    command = (
                        command[len(phrase):]
                        .strip()
                    )

                    break


            # User only said:
            # "Jarvis"

            if not command:

                speak(
                    "Yes, how can I help?"
                )

                command = listen()

                if not command:

                    continue

                command = (
                    command.lower()
                    .strip()
                )


            running = process_command(
                command
            )

        else:

            print(
                "Ignored: Wake word not detected."
            )


# ========================
# START JARVIS
# ========================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\nJARVIS stopped by keyboard."
        )

    except Exception as error:

        print(
            "Unexpected error:",
            error
        )

        speak(
            "An unexpected error occurred."
        )





