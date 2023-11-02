# basic test of the RFID reader and our different personas
# uses the "say" command on mac to speak the text

import os

def speak(text,voice=""):
    print("\n " + text)
    os.system("say -r160 -v '"+voice + "' " + text)

def read_rfid():
    personas = {
        "0004632310": {"name": "Biene", "prompt": "summ summ summ ich bin die Biene! Frag' mich doch was zu Blumen!", "voice":"Shelley (Deutsch (Deutschland))"},
        "0001427161": {"name": "Roboter", "prompt": "Ich bin ein Roboter, und ich habe einfach immer recht. was ist dein unwichtiges Problem Du Mensch. ha ha ha ha.", "voice":"Grandpa (Deutsch (Deutschland))"},
        "0004663272": {"name": "Currywurst", "prompt": "Ick bin die original Berliner Currywurst. Keule, dit jeht jaarnüscht, dass Du hier stehst und dich uffspielen tust, aber na jut schiess los ", "voice":"Eddy (Deutsch (Deutschland))"},
        "0001384652": {"name": "Schatzkiste", "prompt": "Ich bin die Schatzkiste. Ich bin voller Schätze, aber ich bin auch voller Geheimnisse. Was willst du wissen?", "voice":"Markus"},
        "0001416771": {"name": "Yoda", "prompt": "Yoda ich bin. Kleiner grüner Mann, mit Lichtschwert und Grundschulkenntnissen Grammatik deutsch.", "voice":""},
        }
    rfid_code = input()
    return personas[rfid_code]
    
def main():
    while True:
        persona = read_rfid()
        prompt = persona["prompt"].replace("'", r"\'")
        voice = persona["voice"]
        speak(prompt,voice)


if __name__ == "__main__":
    main()

