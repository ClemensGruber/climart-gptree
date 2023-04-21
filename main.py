# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, subprocess
from dotenv import load_dotenv
import openai
from utils.helpers import *


def transcribe_audio(filename):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript.text)
    return transcript.text



# ------------------------------

def main():
    # Load environment variables from .env file
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # config
    filename_input = "audio/input.wav"
    filename_output = "audio/output.mp3"
    personas = load_json("personas.json")
    
    while True:
        code = input()
        if code == "q":
            break
        else:
            persona = personas[code]
            if persona["name"] == "Biene":
                subprocess.Popen(["afplay", "audio/personas/bee/greetings.mp3"])

    #transcribe_audio(filename_input)
    # greeting audio is in a subprocess in order not to block the main thread 
    


if __name__ == '__main__':
    main()