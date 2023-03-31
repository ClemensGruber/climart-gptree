# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import os
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv


def speak(text):
    #voice = "-v 'Eddy (Deutsch (Deutschland))'"
    voice = ""
    print("\n " + text)
    os.system("say -r180 "+voice + " " + text)


def record_audio(filename="output.wav"):
    fs = 22050  # Sample rate
    seconds = 10  # Duration of recording

    print("\nUm eine Frage zu stellen, drücke die Eingabetaste.")
    print("Drücke die Eingabetaste erneut, um die Frage zu beenden.")
    input()
    print("\nBegin recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs,
                         channels=1)
    input()
    sd.stop()
    print("End recording")
    write(filename, fs, myrecording)  # Save as WAV file


def transcribe_audio(filename="output.wav"):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print("Ich habe folgendes verstanden:")
    print(transcript.text)
    return transcript.text


def query_chatgpt(prompt):
    messages = []
    messages.append(
        {"role": "system", "content": "Be precise, be concise, be polite and positive."})

    message = prompt
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    return reply


def main():
    os.system("clear")
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    soundfile_name = "output.wav"

    print("Hallo ich bin der Awesomebot vom CityLAB Berlin!")

    while True:
        record_audio(soundfile_name)
        prompt = transcribe_audio(soundfile_name)
        reply = query_chatgpt(prompt)
        speak(reply)


if __name__ == '__main__':
    main()
