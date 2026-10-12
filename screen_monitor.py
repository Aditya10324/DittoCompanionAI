import time
import random

def detect_screen_event():
    # Simulate random events for testing
    time.sleep(10)
    return random.choice(["win", "pause", "focus", None])
