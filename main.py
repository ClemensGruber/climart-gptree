# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, subprocess, random, time
from dotenv import load_dotenv
from openai import OpenAI
from utils.helpers import load_json
from utils.weather import add_current_context
from utils.recording import record_audio
from utils.gtts_synthing import synthing
import pyaudio

def play_audio_on_device(device_index, audio_file_path):
    p = pyaudio.PyAudio()

    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=False,
            output=True,
            output_device_index=device_index,
        )

        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()

        stream.start_stream()
        stream.write(audio_data)

        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        p.terminate()


def transcribe_audio(client, filename):
    start = time.time()
    audio_file = open(filename, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    display("Transcription took " + str(time.time() - start) + " seconds.")
    return transcript.text

def display(text):
    os.system('clear')
    print(text)

def query_chatgpt(client, text,system,history):
    start = time.time()
    MAX_CONTEXT_QUESTIONS = 10
    messages = []
    messages.append(
        {"role": "system", "content": system})
    
    for question, answer in history[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })

    messages.append({"role": "user", "content": text})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response.choices[0].message.content
    return reply

    #for chunk in client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, stream=True):
    #    if (text_chunk := chunk.choices[0]["delta"].content):
    #         yield text_chunk

# ------------------------------

def main():
    # Load environment variables from .env file
    load_dotenv()
    # not needed in new interface
    #openai.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    history = []

    # config
    filename_input = "audio/input.wav"
    filename_output = "audio/output.mp3"
    personas = load_json("personas.json")

    options = [f"{code} = {persona['name']}" for code, persona in personas.items()]
    code = input(f"Optionen: {', '.join(options)}, q für Beenden. \n")

    if code == "q":
        display("Programm beendet.")
        return
    else:
        # check if code has a persona
        # and greet the user
        if code in personas:
            persona = personas[code]

            greetings = "audio/personas/" + persona["path"] + "/" +  random.choice(persona["greetings"])["filename"]
            #print(greetings)
            #os.system(f"afplay {greetings}")
            os.system(f"ffplay -v 0 -nodisp -autoexit {greetings}")
        else:
            display("Input not recognized: " + code)

        while True:
            # record audio
            display("recording...")
            record_audio(filename_input)
            display("recording stopped.")

            # play wait sound while api calls are made
            wait = os.getcwd() + "/audio/personas/" + persona["path"] + "/" + random.choice(persona["wait"])["filename"]
            #subprocess.Popen(["afplay", wait])
            #subprocess.Popen(["ffplay -v 0 -nodisp -autoexit", wait])
            os.system(f"ffplay -v 0 -nodisp -autoexit {wait}")

            # transcribe audio to text with whisper-1 model
            user_text = transcribe_audio(client, filename_input)
            display(user_text)

            if "Ende" not in user_text:
                # generate response from text with GPT-3 model
                system_context=add_current_context(persona["prompt"])
                ai_response = query_chatgpt(client, user_text,system_context,history)
                history.append((user_text, ai_response))
                display(ai_response)
                synthing(client, ai_response,filename_output)

                # play audio response
                #^  os.system(f"afplay {filename_output}")
                os.system(f"ffplay -v 0 -nodisp -autoexit {filename_output}")
            else:
                byebye = "audio/personas/" + persona["path"] + "/" + random.choice(persona["bye"])["filename"]
                #os.system(f"afplay {byebye}")
                os.system(f"ffplay -v 0 -nodisp -autoexit {byebye}")
                main()
   
# ------------------------------

if __name__ == '__main__':
    main()