import pyaudio
import wave
import os
from elevenlabs import ElevenLabs
from scipy.io.wavfile import write


def synth_speech(text):
    eleven = ElevenLabs(os.getenv("ELEVENLABS_API_KEY"))
    # Get a Voice object, by name or UUID
    voice = eleven.voices["Bella"]
    # Generate the TTS
    audio = voice.generate(text)
    # Save the TTS to a file named 'my_first_tts' in the working directory
    audio.save("output_tts")

def play_audio():
    os.system("afplay " + "output_tts.mp3")