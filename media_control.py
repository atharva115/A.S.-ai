import pygame
from common import speak

def play_music(file_path: str):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        speak("Playing music.")
    except Exception as e:
        speak(f"Unable to play music: {e}")
        
