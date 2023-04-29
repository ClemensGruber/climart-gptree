# audio file generator
# generates local audio files based on the text and file names
# specified in the personas.json file
# to be used as a way to reduce waiting time while API calls are made
# usage: python3 audiofile-generator.py
# exports: audio files in the audio/personas folder

from helpers import *
from gtts_synthing import synthing

def generate_audio(personas):
    # iterate over all personas from the json file
    for key, persona in personas.items():
      print(persona["name"])
    
    #synthing(text, filename)


if __name__ == "__main__":
    personas = load_json("../personas.json")
    generate_audio(personas)