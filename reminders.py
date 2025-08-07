import json
import schedule
import re
from mycommon import speak

REMINDERS_FILE = "data/reminders.json"

def load_reminders():
    try:
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reminders(reminders_list):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders_list, f, indent=2)

def notify_reminder(message):
    speak(f"Reminder: {message}")
    return schedule.CancelJob  # run once and cancel

def set_reminder(command: str):
    """
    Parse reminder commands like:
    "set reminder to take medicine in 10 minutes"
    or
    "set reminder to call mom in 2 hours"
    """
    pattern = r"reminder to (.+) in (\d+) (minute|minutes|hour|hours)"
    match = re.search(pattern, command)
    if not match:
        speak("Sorry, I couldn't understand the reminder. Please say it like 'set reminder to <task> in <number> minutes or hours.'")
        return

    message = match.group(1).strip()
    number = int(match.group(2))
    unit = match.group(3)

    reminders = load_reminders()
    reminders.append({"message": message, "time": f"{number} {unit}"})
    save_reminders(reminders)

    speak(f"Setting a reminder to {message} in {number} {unit}.")

    if "hour" in unit:
        schedule.every(number).hours.do(notify_reminder, message=message)
    else:
        schedule.every(number).minutes.do(notify_reminder, message=message)
