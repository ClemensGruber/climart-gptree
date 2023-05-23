# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, random
from dotenv import load_dotenv
import openai
from utils.helpers import display, load_json, clear, time_it, play_sound, chat_bubble, chat_bubble_user, welcome
from utils.recording import record_audio
from utils.gtts_synthing import synthing

@time_it
def transcribe_audio(filename):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text


@time_it
def query_chatgpt(text,system,history):
    MAX_CONTEXT_QUESTIONS = 10
    messages = []
    messages.append(
        {"role": "system", "content": system})
    
    for question, answer in history[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })

    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    return reply

# ------------------------------

def main():
    # Load environment variables from .env file
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # config
    filename_input = "audio/input.wav"
    filename_output = "audio/output.mp3"
    personas = load_json("personas.json")
    SYSTEM = "green"
    USER = "yellow"
    BOT = "white"
    ERROR = "red"

    end_words = ["Ende","Auf Wiedersehen","Wechseln","Tschüss","Bye","End","Quit","Exit","end."]

    play_sound("audio/boot/"+str(random.randint(1,7))+".mp3",False)
    clear()

    display(welcome(), color=SYSTEM)
    chat_bubble(text="Hallo, ich bin der Kiezbot!\nBitte wähle eine Persona aus.\nSprich 'Ende', wenn Du das Gespräch beenden möchtest. \nViel Spaß!",who="Kiezbot")
    
    display("Optionen: 1 = Biene, 2 = Roboter, 3 = Currywurst", color=SYSTEM)

    while True:
        history = []
        code = input()

        if code == "q":
            display("Programm beendet.", color=SYSTEM)
            break
        else:
            # check if code has a persona
            # and greet the user
            if code in personas:
                persona = personas[code]
                random_selection = persona["greetings"][random.randint(0,len(persona["greetings"])-1)]
                file = "audio/personas/" + persona["path"] + "/" +  random_selection["filename"]
                chat_bubble(text=random_selection["text"],who=persona["name"])
                play_sound(file)
                
            else:
                display("Input not recognized: "+ code, color=ERROR)

            while True:
                # record audio
                display("recording...",color=ERROR)
                record_audio(filename_input)
                display("recording stopped.",color=ERROR)

                # transcribe audio to text with whisper-1 model
                user_text = transcribe_audio(filename_input)
                chat_bubble_user(text=user_text)
                
                if not any(word in user_text for word in end_words):
                    # play wait sound while api calls are made
                    random_selection = persona["wait"][random.randint(0,len(persona["wait"])-1)]
                    file = "audio/personas/" + persona["path"] + "/" +  random_selection["filename"]
                    chat_bubble(text=random_selection["text"],who=persona["name"])
                    play_sound(file,False)

                    # generate response from text with GPT-3 model
                    ai_response = query_chatgpt(user_text,persona["prompt"],history)
                    history.append((user_text, ai_response))
                    chat_bubble(text=ai_response,who=persona["name"])
                    
                    # convert response to audio with google text-to-speech model
                    synthing(ai_response,filename_output,persona["tts_settings"])

                    # play audio response
                    play_sound(filename_output)
                
                else:
                    random_selection = persona["bye"][random.randint(0,len(persona["bye"])-1)]
                    file = "audio/personas/" + persona["path"] + "/" +  random_selection["filename"]
                    chat_bubble(text=random_selection["text"],who=persona["name"])
                    play_sound(file)
                    main()
   
# ------------------------------

if __name__ == '__main__':
    main()