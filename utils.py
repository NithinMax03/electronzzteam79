from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from dialogue_engine import chat_with_character  # Make sure dialogue_engine.py is present

def generate_dialogue(name, traits, scenario, tone):
    prompt = (
        f"You are {name}, a character with the traits: {traits}.\n"
        f"Scenario: {scenario}.\n"
        f"Your tone should be: {tone}.\n"
        "Generate a multi-sentence emotional RPG-style dialogue."
    )
    return chat_with_character(prompt)

def translate_text(text, target_lang="ta"):
    return GoogleTranslator(source='auto', target=target_lang).translate(text)

def text_to_audio(text):
    tts = gTTS(text)
    path = "media/voice.mp3"
    tts.save(path)
    return path
