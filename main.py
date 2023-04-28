# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, subprocess, random
from dotenv import load_dotenv
import openai
import pyaudio
from scipy.io.wavfile import write
import numpy as np
from utils.helpers import *

def record_audio(filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 1000  # Adjust this value to set the sensitivity of the voice detection
    SILENCE_LIMIT = 1.1  # Number of seconds of silence before stopping the recording

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Wait for the user to start speaking
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        if np.abs(data).mean() > THRESHOLD: #check mean amplitude of the chunk
            break

    # Record until the user stops speaking
    frames = []
    silent_frames = 0
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        frames.append(data)
        if np.abs(data).mean() < THRESHOLD:
            silent_frames += 1
        else:
            silent_frames = 0
        if silent_frames > SILENCE_LIMIT * RATE / CHUNK:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert the frames to a single audio file
    frames = np.concatenate(frames, axis=0)
    write(filename, RATE, frames)

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
              greetings = "audio/personas/" + persona["path"] + "/" + random.choice(persona["greetings"])
              os.system("afplay " + greetings)
            else:
                display("Input not recognized: "+ code)

            # record audio
            # todo: implement Julias code
            display("recording...")
            record_audio(filename_input)
            display("recording stopped.")

            # play wait sound while api calls are made
            wait = "audio/personas/" + persona["path"] + "/" + random.choice(persona["wait"])
            subprocess.Popen(["afplay", wait])

            # transcribe audio to text with whisper-1 model
            user_text = transcribe_audio(filename_input)
            display(user_text)

            # generate response from text with GPT-3 model
            ai_response = query_chatgpt(user_text,persona)
            display(ai_response)

            # convert response to audio with google text-to-speech model
            # todo: implement Julias code

            # play audio response
            # subprocess.Popen(["afplay", filename_output])

    
   
# ------------------------------

if __name__ == '__main__':
    main()