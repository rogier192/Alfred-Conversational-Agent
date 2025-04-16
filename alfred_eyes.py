import os
import sys
import signal
# import pvporcupine
import pyaudio
import struct
import pygame
import time
import random
from transformers import pipeline
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Configuratie
AGENT_ID = os.environ.get('AGENT_ID', 'CGLDLtk4sc6MYFurfAFB')  # Vervang met jouw Agent ID
API_KEY = os.environ.get('ELEVENLABS_API_KEY', 'sk_c94c2d13d1247cf0cc7e765c2975f5f9914ca65584058d53')  # **VEILIG BEWAREN!**
WAKE_WORD = "Hey Alfred"

# 🎭 Emotie-analyse model laden (lokaal met Hugging Face)
emotion_analyzer = pipeline("sentiment-analysis")

# 🎨 Kleuren per emotie
colors = {
    "happy": (0, 255, 0),    # Groen
    "angry": (255, 0, 0),    # Rood
    "neutral": (0, 0, 255)   # Blauw
}

# 🎬 Pygame setup voor de ogen
pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Alfred's Eyes")

def detect_emotion(text):
    """ Analyseert tekst en bepaalt emotie (happy, angry, neutral). """
    result = emotion_analyzer(text)[0]  # Model analyseert tekst
    label = result["label"].lower()

    if "positive" in label:
        return "happy"  # Groen
    elif "negative" in label:
        return "angry"  # Rood
    else:
        return "neutral"  # Blauw

def show_eyes(emotion):
    """ Tekent de ogen op basis van de emotie. """
    eye_color = colors.get(emotion, (255, 255, 255))  # Standaard wit
    eye_x = 100
    running = True
    start_time = time.time()

    while running:
        screen.fill((0, 0, 0))  # Zwarte achtergrond
        eye_x += random.randint(-3, 3)  # Willekeurige beweging

        pygame.draw.circle(screen, eye_color, (eye_x, 100), 40)  # Linkeroog
        pygame.draw.circle(screen, eye_color, (eye_x + 200, 100), 40)  # Rechteroog

        pygame.display.flip()

        if random.random() < 0.1:  # 10% kans om te knipperen
            time.sleep(0.1)
            screen.fill((0, 0, 0))
            pygame.display.flip()
            time.sleep(0.1)

        if time.time() - start_time > 3:  # Stop na 3 seconden
            running = False

    pygame.quit()

# Wake-word engine starten
def detect_wake_word():
    porcupine = pvporcupine.create(
        access_key="YOUR_PICOVOICE_ACCESS_KEY",
        keyword_paths=["hey_alfred.ppn"]
    )
    
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🎤 Say 'Hey Alfred' to activate...")
    
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("✅ Wake-word detected! Starting Alfred...")
            break

    audio_stream.close()
    pa.terminate()
    porcupine.delete()

# ElevenLabs conversatie starten + ogen laten reageren
def start_conversation():
    client = ElevenLabs(api_key=API_KEY)
    conversation = Conversation(
        client,
        AGENT_ID,
        requires_auth=bool(API_KEY),
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=process_response,  # Emotie-analyse hier koppelen!
        callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
    )
    conversation.start_session()
    
    signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
    conversation_id = conversation.wait_for_session_end()
    print(f"Conversation ID: {conversation_id}")

def process_response(response):
    """ Koppelt emotie-analyse aan de ogen. """
    emotion = detect_emotion(response)  # Vraag AI om emotie
    show_eyes(emotion)  # Toon de juiste ogen op het scherm
    print(f"Agent: {response}")  # Laat de robot praten

if __name__ == "__main__":
    # detect_wake_word()
    start_conversation()
