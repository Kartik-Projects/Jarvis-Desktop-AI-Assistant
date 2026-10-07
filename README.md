# JARVIS - Python Voice Assistant

JARVIS is a Python-based voice assistant for Windows. It listens to voice commands, performs specific computer tasks, and uses the OpenAI API to answer general questions.

## Features

* Voice command recognition using SpeechRecognition
* Voice responses using Windows SAPI.SpVoice
* Wake word detection using:

  * `Jarvis`
  * `Hey Jarvis`
  * `Hi Jarvis`
* Current time
* Current date
* Open websites
* Open Windows applications
* Play songs on YouTube
* Search YouTube
* Pause YouTube playback
* Resume YouTube playback
* Increase system volume
* Decrease system volume
* Mute system volume
* Unmute system volume
* Take screenshots
* Answer general questions using the OpenAI API
* Stop JARVIS using voice commands

## Websites

JARVIS can open the following websites:

* YouTube
* Google
* Facebook
* LinkedIn
* GitHub
* Instagram
* Gmail
* WhatsApp

Example:

```text
Jarvis, open YouTube
```

## Windows Applications

JARVIS can open:

* Notepad
* Calculator
* Paint

Example:

```text
Jarvis, open Notepad
```

## YouTube Commands

Play a song:

```text
Jarvis, play Believer
```

Search YouTube:

```text
Jarvis, search YouTube for Python tutorials
```

Pause playback:

```text
Jarvis, pause the song
```

Resume playback:

```text
Jarvis, resume the song
```

## Time and Date

Ask for the current time:

```text
Jarvis, what is the time?
```

Ask for the current date:

```text
Jarvis, what is today's date?
```

## Volume Control

Increase volume:

```text
Jarvis, increase volume
```

Decrease volume:

```text
Jarvis, decrease volume
```

Mute:

```text
Jarvis, mute the computer
```

Unmute:

```text
Jarvis, unmute the computer
```

## Screenshot

JARVIS can take a screenshot of the computer screen.

Example:

```text
Jarvis, take a screenshot
```

Screenshots are saved in:

```text
Pictures/JARVIS Screenshots/
```

The screenshot filename contains the date and time.

## OpenAI Integration

JARVIS uses the OpenAI API to answer general questions that are not handled by its built-in commands.

Example:

```text
Jarvis, explain Python
```

The OpenAI API key is loaded from the `.env` file.

```env
OPENAI_API_KEY=your_api_key_here
```

## Requirements

* Windows
* Python
* Microphone
* Internet connection
* OpenAI API key

## Installation

Install the required Python packages:

```bash
pip install openai SpeechRecognition pywin32 pyautogui pywhatkit python-dotenv PyAudio
```

Create a `.env` file in the project folder:

```env
OPENAI_API_KEY=your_api_key_here
```

Run JARVIS:

```bash
python jarvis.py
```

## Stop JARVIS

JARVIS can be stopped using commands such as:

```text
Jarvis, stop
```

```text
Jarvis, exit
```

```text
Jarvis, goodbye
```

## Project Technologies

* Python
* OpenAI API
* SpeechRecognition
* Windows SAPI
* PyAutoGUI
* PyWhatKit
* python-dotenv
* PyWin32
* Webbrowser
* Subprocess
