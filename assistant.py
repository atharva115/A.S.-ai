import speech_recognition as sr
import schedule
import time
import os
from common import speak
from commands import reminders, media_control, file_manager

recognizer = sr.Recognizer()

def listen() -> str:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak("Listening...")
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            # Using online Google Recognizer here; for offline change the recognizer accordingly
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            speak("Listening timed out, please try again.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech recognition service is unavailable. I am offline.")
    return ""

def execute_command(command: str):
    if "reminder" in command:
        reminders.set_reminder(command)
    elif "play music" in command:
        music_path = os.path.join("resources", "sample_music.mp3")
        if os.path.exists(music_path):
            media_control.play_music(music_path)
        else:
            speak("Sorry, music file not found.")
    elif "search file" in command:
        file_manager.search_file(command)
    elif command.strip() in {"stop", "exit", "quit"}:
        speak("Goodbye!")
        exit()
    else:
        speak("That command is not available offline or not recognized.")

def run_scheduled_tasks():
    schedule.run_pending()

def main():
    # Ensure data folder & reminders file exist
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.isfile("data/reminders.json"):
        with open("data/reminders.json", "w") as f:
            f.write("[]")

    speak("Welcome! I am your offline assistant.")

    while True:
        command = listen()
        if command:
            execute_command(command)
        run_scheduled_tasks()
        time.sleep(1)

if __name__ == "__main__":
    main()
