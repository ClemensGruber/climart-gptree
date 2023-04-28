# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, subprocess, random
from dotenv import load_dotenv
import openai
from utils.helpers import *


def transcribe_audio(filename):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text

def display(text):
    print(text)

def query_chatgpt(text,persona):
    messages = []
    messages.append(
        {"role": "system", "content": persona["prompt"]})

    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    return reply

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
            display("Programm beendet.")
            break
        else:
            # check if code has a persona
            # and greet the user
            if code in personas:
              persona = personas[code]
              greetings = "audio/personas/" + persona["path"] + "/" + random.choice(persona["greetings"])
              subprocess.Popen(["afplay", greetings])
            else:
                display("Input not recognized: "+ code)

            # record audio
            # todo: implement Julias code

            # transcribe audio to text with whisper-1 model
            user_text = transcribe_audio(filename_input)
            display(user_text)

            # generate response from text with GPT-3 model
            ai_response = query_chatgpt(user_text,persona)
            display(ai_response)

            # convert response to audio with google text-to-speech model
            # todo: implement Julias code

            # play audio response
            subprocess.Popen(["afplay", filename_output])

    
   
# ------------------------------

if __name__ == '__main__':
    main()