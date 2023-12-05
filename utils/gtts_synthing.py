# text to speech api for kiezbot
# expects: text, filename, settings
# returns: audio file

"""Google Cloud Text-To-Speech API sample application .
"""


def string_to_enum(enum_class, enum_string):
    enum_parts = enum_string.split('.')
    enum_obj = getattr(enum_class, enum_parts[-1])
    return enum_obj


def synthing(client, text,filename):
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    response.stream_to_file(filename)