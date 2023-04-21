
# This function reads in either an RFID Code or a Keyboard input from 1-5 and 
# returns the character code for use in the character_prompts.py
# Current character codes:
# 0: KiKi, die Biene
# 1: RoKi, der Roboter
# 2: KiRi-Wurst
# 3: Schaki, die Schatztruhe
# 4: Kleine grüne Mann aka Yoda 


def getCharacter(code):
    characterRFID = {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "0004632310": 0, 
    "0001427161": 1,
    "0004663272": 2,
    "0001384652": 3,
    "0001416771": 4
    }

    if code in characterRFID:
        return characterRFID[code]
    else:
        return "Invalid character code " + code
