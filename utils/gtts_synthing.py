#!/usr/bin/env python
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All Rights Reserved.

"""Google Cloud Text-To-Speech API sample application .
"""

def synthing(text):
    """Synthesizes speech from the input string of text or ssml.
    Make sure to be working in a virtual environment.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech
    
    client = texttospeech.TextToSpeechClient()

    # text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # select a language, model and gender 
    voice = texttospeech.VoiceSelectionParams(
        language_code="de-DE", name="de-DE-Neural2-F", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # specific config for the honeybee voice
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, 
        speaking_rate=1.2, 
        pitch=7
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output_gtts.mp3", "wb") as out:
        # Write the response to output_gtts file.
        out.write(response.audio_content)
        print('Audio content written to file "output_gtts.mp3"')
    # [END tts_quickstart]

if __name__ == "__main__":
    synthing(text="Hello, you cute little honeybee.")
