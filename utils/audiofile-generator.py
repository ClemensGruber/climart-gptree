# audio file generator
# generates local audio files based on the text and file names
# specified in the personas.json file
# to be used as a way to reduce waiting time while API calls are made
# usage: python3 audiofile-generator.py
# exports: audio files in the audio/personas folder
# needs to run manually only when new files should be generated

from helpers import load_json
from gtts_synthing import synthing

def generate_audio(personas,type="greetings"):
    # iterate over all personas from the json file
    for key, persona in personas.items():
      settings = persona["tts_settings"]
      
      for item in persona[type]:
        text = item["text"]
        filename = "./audio/personas/" + persona["path"] + "/" + item["filename"]
        print(text)
        print(filename)
        synthing(text, filename, settings)

if __name__ == "__main__":
    personas = load_json("../personas.json")
    generate_audio(personas,type="greetings")
    generate_audio(personas,type="idle")
    generate_audio(personas,type="wait")
    generate_audio(personas,type="bye")