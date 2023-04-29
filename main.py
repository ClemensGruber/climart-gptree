# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, subprocess, random, time
from dotenv import load_dotenv
import openai
from utils.helpers import *
from utils.recording import record_audio
from utils.gtts_synthing import synthing


def transcribe_audio(filename):
    start = time.time()
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    display("Transcription took " + str(time.time() - start) + " seconds.")
    return transcript.text

def display(text):
    print(text)

def query_chatgpt(text,persona):
    start = time.time()
    messages = []
    messages.append(
        {"role": "system", "content": persona["prompt"]})

    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    display("ChatGPT took " + str(time.time() - start) + " seconds.")
    return reply

# ------------------------------

def main():
    display("Optionen: 1 = Biene, 2 = Roboter, 3 = Currywurst")
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

              greetings = "audio/personas/" + persona["path"] + "/" +  random.choice(persona["greetings"])["filename"]
              print(greetings)
              os.system("afplay " + greetings)
            else:
                display("Input not recognized: "+ code)

            # record audio
            display("recording...")
            record_audio(filename_input)
            display("recording stopped.")

            # play wait sound while api calls are made
            wait = "audio/personas/" + persona["path"] + "/" + random.choice(persona["wait"])["filename"]
            subprocess.Popen(["afplay", wait])

            # transcribe audio to text with whisper-1 model
            user_text = transcribe_audio(filename_input)
            display(user_text)

            # generate response from text with GPT-3 model
            ai_response = query_chatgpt(user_text,persona)
            display(ai_response)

            # convert response to audio with google text-to-speech model
            synthing(ai_response,filename_output,persona["tts_settings"])

            # play audio response
            subprocess.Popen(["afplay", filename_output])

    
   
# ------------------------------

if __name__ == '__main__':
    main()