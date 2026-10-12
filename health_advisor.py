import speech_recognition as sr
from transformers import pipeline

recognizer = sr.Recognizer()
nlp = pipeline("text-generation", model="distilgpt2")

def listen_and_respond():
    with sr.Microphone() as source:
        print("Listening for health queries...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            if "stress" in text or "tired" in text:
                print("Take a deep breath. Maybe stretch a bit?")
            elif "exercise" in text:
                print("Let’s plan a short walk or workout!")
            else:
                response = nlp(text, max_length=50)[0]["generated_text"]
                print(response)
        except sr.UnknownValueError:
            print("Sorry, I didn’t catch that.")
