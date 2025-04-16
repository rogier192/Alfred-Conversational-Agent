import os
import sys
import signal
import pvporcupine
import pyaudio
import struct
import subprocess
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Configuratie
AGENT_ID = os.environ.get('AGENT_ID', 'YyQP7lkk3zhwSe9BYnDd')  # Vervang met jouw Agent ID
API_KEY = os.environ.get('ELEVENLABS_API_KEY', 'faTc7Z6O4jsv97+Ve1HJEb9iwxTR+Soos+PMiapgdNE+JylEJMNGqw==')  # **VEILIG BEWAREN!**
WAKE_WORD = "Hey Alfred"

# master process to control current volume

# Wake-word engine starten
def detect_wake_word():
    porcupine = pvporcupine.create(
        access_key="YOUR_PICOVOICE_ACCESS_KEY",  # Onze API-key bij Picovoice
        keyword_paths=[pvporcupine.KEYWORD_PATHS["hey-alfred"]]
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

# ElevenLabs conversatie starten
def start_conversation():
    client = ElevenLabs(api_key=API_KEY)
    conversation = Conversation(
        client,
        AGENT_ID,
        requires_auth=bool(API_KEY),
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=lambda response: print(f"Agent: {response}"),
        callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
    )
    conversation.start_session()
    
    signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
    conversation_id = conversation.wait_for_session_end()
    print(f"Conversation ID: {conversation_id}")

if __name__ == "__main__":
    detect_wake_word()
    start_conversation()
