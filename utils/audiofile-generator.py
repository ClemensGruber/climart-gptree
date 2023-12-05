# audio file generator
# generates local audio files based on the text and file names
# specified in the personas.json file
# to be used as a way to reduce waiting time while API calls are made
# usage: python3 audiofile-generator.py
# exports: audio files in the audio/personas folder
# needs to run manually only when new files should be generated

from helpers import load_json
from gtts_synthing import synthing
import os
from dotenv import load_dotenv
from openai import OpenAI

def generate_audio(client, personas,type="greetings"):
    # iterate over all personas from the json file
    for key, persona in personas.items():
      settings = persona["tts_settings"]
      
      for item in persona[type]:
        text = item["text"]

        path = "./audio/personas/" + persona["path"]
        if not os.path.exists(path):
          os.makedirs(path)

        filename = path + "/" + item["filename"]
        print(text)
        print(filename)
        synthing(client, text, filename)

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI()

    personas = load_json("../personas.json")
    generate_audio(client, personas,type="greetings")
    generate_audio(client, personas,type="wait")
    generate_audio(client, personas,type="bye")