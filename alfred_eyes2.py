import os
import sys
import subprocess
import signal
import pvporcupine
import pyaudio
import websockets.exceptions
import struct
import pygame
import time
import threading
from RoboEyesLibrary import eyes, DEFAULT, TIRED, ANGRY, HAPPY, SLEEPY
from transformers import pipeline
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from queue import Queue

"""
Elevenlabs account:
alfred-social-robot@gmx.com
Password:
WeLoveAlfred123!

Email:
alfred-social-robot@gmx.com
Password:
WeLoveAlfred
"""

# setup a queue
emotion_queue = Queue()

# # api keys, for convenience. Could be put into environment file of user service.
AGENT_ID = os.environ.get('AGENT_ID', 'YLvH9Grqjw2BJ9XdT15a')  # This is the agent you set in elevenlabs
API_KEY = os.environ.get('ELEVENLABS_API_KEY', 'sk_0c3b122515480691b3984f3ddaca0f0df10998463670a022')  # This is the API key to Elevenlabs
PICOVOICE_KEY = os.environ.get('PICOVOICE_API_KEY', 'faTc7Z6O4jsv97+Ve1HJEb9iwxTR+Soos+PMiapgdNE+JylEJMNGqw==')
WAKE_WORD_PATH = os.environ.get('WAKE_WORD_PATH', 'hey_alfred.ppn')
WAKE_WORD = "Hey Alfred"

# Local emotion analyser pipeline from Huggingface
# sentiment analysis is lightweight and identifies negative, neutral or positive
emotion_analyzer = pipeline("sentiment-analysis")

# Emotion mapping with all displayable emotions from the library
EMOTION_MAP = {
    'negative': ANGRY,
    'neutral': DEFAULT,
    'positive': HAPPY,
    'verdrietig': TIRED,
    'slaperig': SLEEPY
}

# Global variables
current_emotion = DEFAULT  # what Alfred should be displaying after display flip
running = True
awake = False  # Sleep state to True when Alfred hears Wake Word "Hey Alfred"


# Pygame setup
pygame.init()
pygame.display.init()
print(pygame.display.get_driver())
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Alfred's Eyes")

def increase_speaker_volume():
    proc = subprocess.Popen('wpctl set-volume -l 1 @DEFAULT_SINK@ 10%+', shell=True, stdout=subprocess.PIPE)
    proc.wait()


def decrease_speaker_volume():
    proc = subprocess.Popen('wpctl set-volume -l 1 @DEFAULT_SINK@ 10%-', shell=True, stdout=subprocess.PIPE)
    proc.wait()


def set_speaker_volume(target):
    proc = subprocess.Popen('wpctl set-volume -l 1 @DEFAULT_SINK@ {target}%', shell=True, stdout=subprocess.PIPE)
    proc.wait()


def detect_emotion(text):  # detect emotion uses Huggingface pipeline to analyse LLM output text
    result = emotion_analyzer(text)[0]
    label = result["label"].lower()

    if label in EMOTION_MAP:
        return EMOTION_MAP[label]

    else:
        return EMOTION_MAP["neutral"]

# most of this method and the library is from the mechatronics team at Delft
def show_eyes():
    global running, current_emotion, awake
    try:
        # Hoofdloop in main thread
        while running:
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            if not running:
                break

            try:
                # Update eyes
                if awake:
                    eyes(0, 0, mood=current_emotion, selfEmote=False, selfMove=False)
                    # pygame.display.flip()

                else:
                    eyes(0, 0, mood=SLEEPY, selfEmote=False, selfMove=False)

            except Exception as e:
                print(f"Error updating eyes: {e}")
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        running = False
        pygame.quit()
        sys.exit(0)

# Start Wake Word engine
def detect_wake_word():
    global awake
    # Uses Picovoice to detect and generate Wake Words
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_KEY,
        keyword_paths=[WAKE_WORD_PATH]
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    try:
        print("🎤 Say 'Hey Alfred' to activate...")

        # Loops until wake word is said
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("✅ Wake-word detected! Starting Alfred...")
                awake = True  # wakes up
                break

    except Exception as e:
        print(f"Error in wake word detection: {e}")

    finally:
        if audio_stream is not None:
            audio_stream.stop_stream()
            audio_stream.close()
        pa.terminate()
        if porcupine is not None:
            porcupine.delete()


# Start the Elevenlabs conversation
def conversation_thread():
    global running
    detect_wake_word()  # conversation only continues after Wake Word is said

    try:
        client_tools = ClientTools()
        client_tools.register("increaseVolume", increase_speaker_volume)
        client_tools.register("decreaseVolume", decrease_speaker_volume)
        client_tools.register("setVolume", set_speaker_volume)

        client = ElevenLabs(api_key=API_KEY)
        conversation = Conversation(
            client,
            AGENT_ID,
            requires_auth=bool(API_KEY),
            audio_interface=DefaultAudioInterface(),
            client_tools=client_tools,
            callback_agent_response=process_response,  # For current emotion
            callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
        )
    
        conversation.start_session()
        conversation_id = conversation.wait_for_session_end()
        print(f"Conversation ID: {conversation_id}")
        time.sleep(0.5)  # give pygame time to shut down
        running = False


# process exceptions to clean output
    except websockets.exceptions.ConnectionClosedOK:
        print("conversation closed websocket")
        time.sleep(0.5)  # give pygame time to shut down
        running = False

    except Exception as excpt:
        print(excpt)
        if "ConnectionClosedOK" in str(excpt):
            print("conversation closed")
        else:
            print(f"error is conversation thread: {excpt}")
        time.sleep(0.5)  # give pygame time to shut down
        running = False


# Analyses and outputs current response to text, also connects to Alfred Eyes
def process_response(response):
    global current_emotion
    current_emotion = detect_emotion(response)  # Analyse response for current emotion
    print(f"Alfred feels {current_emotion}")
    print(f"Agent: {response}")
    emotion_queue.put((current_emotion, response))


def handle_shutdown(sig, frame):
    global running
    print("shutting down")
    running = False


# main runs 2 threads, a main thread for the graphical tasks and a thread for the conversation
def main():
    signal.signal(signal.SIGINT, handle_shutdown)
    threading.Thread(target=conversation_thread, daemon=True).start()
    show_eyes()  # must run on main


if __name__ == "__main__":
    main()
