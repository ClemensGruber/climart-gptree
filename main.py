# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, random
from dotenv import load_dotenv
import openai
from utils.helpers import display, load_json, clear, time_it, play_sound, chat_bubble, chat_bubble_user, welcome
from utils.recording import record_audio
from utils.gtts_synthing import synthing
from utils.gpio import led


def is_linux():
    return os.name == "posix"

#@time_it
def transcribe_audio(filename):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text


#@time_it
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
    LED_GREEN = 4
    LED_RED = 17

    led(LED_GREEN,"off")
    led(LED_RED,"off")

    end_words = ["Ende","Auf Wiedersehen","Wechseln","Tschüss","Bye","End","Quit","Exit","end."]

    play_sound("audio/boot/"+str(random.randint(1,7))+".mp3",False)
    clear()

    display(welcome(), color=SYSTEM)
    chat_bubble(text="Hallo, ich bin der Kiezbot!\nBitte stelle eine der Figuren auf das runde Feld, um mit ihr zu sprechen.\nSage 'Vielen Dank, Ende', wenn Du das Gespräch beenden möchtest. \nViel Spaß!",who="Kiezbot")
    
    
    while True:
        history = []
        code = input()

        if code == "0004632310":
            display("Programm beendet.", color=SYSTEM)
            os.system("sudo shutdown now")
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
                led(LED_RED,"on")
                record_audio(filename_input)
                display("recording stopped.",color=ERROR)
                led(LED_RED,"off")

                # transcribe audio to text with whisper-1 model
                user_text = transcribe_audio(filename_input)
                chat_bubble_user(text=user_text)
                
                if not any(word in user_text for word in end_words):
                    # play wait sound while api calls are made
                    random_selection = persona["wait"][random.randint(0,len(persona["wait"])-1)]
                    file = "audio/personas/" + persona["path"] + "/" +  random_selection["filename"]
                    chat_bubble(text=random_selection["text"],who=persona["name"])
                    led(LED_GREEN,"on")
                    play_sound(file,False)
                    led(LED_GREEN,"off")

                    # generate response from text with GPT-3 model
                    ai_response = query_chatgpt(user_text,persona["prompt"],history)
                    history.append((user_text, ai_response))
                    
                    # convert response to audio with google text-to-speech model
                    synthing(ai_response,filename_output,persona["tts_settings"])
                    chat_bubble(text=ai_response,who=persona["name"])

                    # play audio response
                    led(LED_GREEN,"on")
                    play_sound(filename_output)
                    led(LED_GREEN,"off")
                
                else:
                    random_selection = persona["bye"][random.randint(0,len(persona["bye"])-1)]
                    file = "audio/personas/" + persona["path"] + "/" +  random_selection["filename"]
                    chat_bubble(text=random_selection["text"],who=persona["name"])
                    led(LED_GREEN,"on")
                    play_sound(file)
                    led(LED_GREEN,"off")
                    main()
   
# ------------------------------

if __name__ == '__main__':
    main()