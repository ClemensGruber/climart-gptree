# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, subprocess, random
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
    print("Optionen: 1 = Biene, 2 = Roboter")
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
            # check if code has a persona
            # and greet the user
            if code in personas:
              persona = personas[code]
              greetings = "audio/personas/" + persona["path"] + "/" + random.choice(persona["greetings"])
              subprocess.Popen(["afplay", greetings])
            else:
                print("Input not recognized: "+ code)

    #transcribe_audio(filename_input)
    # greeting audio is in a subprocess in order not to block the main thread 
    


if __name__ == '__main__':
    main()