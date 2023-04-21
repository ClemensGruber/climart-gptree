# Kiezbot
# Conversational bot for the CityLAB Berlin

import os, subprocess
from dotenv import load_dotenv
from utils.helpers import *











# ------------------------------

def main():
    # Load environment variables from .env file
    load_dotenv()
    openai_api_ke = os.getenv("OPENAI_API_KEY")

    # config
    filename_input = "input.wav"
    filename_output = "output.mp3"
    filename_characters = "characters.json"
    text = load_json(filename_characters)


if __name__ == '__main__':
    main()