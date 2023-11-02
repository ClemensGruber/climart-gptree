# text to speech api for kiezbot
# expects: text, filename, settings
# returns: audio file

"""Google Cloud Text-To-Speech API sample application .
"""

def string_to_enum(enum_class, enum_string):
    enum_parts = enum_string.split('.')
    enum_obj = getattr(enum_class, enum_parts[-1])
    return enum_obj

def synthing(text,filename,settings):
    """Synthesizes speech from the input string of text or ssml.
    Make sure to be working in a virtual environment.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech
    
    client = texttospeech.TextToSpeechClient()

    # text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    ssml_gender = string_to_enum(texttospeech.SsmlVoiceGender, settings["ssml_gender"])

    # select a language, model and gender 
    voice = texttospeech.VoiceSelectionParams(
        language_code=settings["language_code"], name=settings["name"], ssml_gender=ssml_gender
    )

    # specific config for the honeybee voice
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, 
        speaking_rate=settings["speaking_rate"], 
        pitch=settings["pitch"]
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(filename, "wb") as out:
        # Write the response to output_gtts file.
        out.write(response.audio_content)
