import pyaudio
from scipy.io.wavfile import write
import numpy as np

def record_audio(filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #RATE = 22050  # samples per second
    RATE = 16000 # for the anker on raspi
    THRESHOLD = 1200  # Adjust this value to set the sensitivity of the voice detection
    SILENCE_LIMIT = 2  # Number of seconds of silence before stopping the recording

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    #input_device_index=audio_device,
                    frames_per_buffer=CHUNK)

    # Wait for the user to start speaking
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        if np.abs(data).mean() > THRESHOLD: #check mean amplitude of the chunk
            break

    # Record until the user stops speaking
    frames = []
    silent_frames = 0
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        frames.append(data)
        if np.abs(data).mean() < THRESHOLD:
            silent_frames += 1
        else:
            silent_frames = 0
        if silent_frames > SILENCE_LIMIT * RATE / CHUNK:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert the frames to a single audio file
    frames = np.concatenate(frames, axis=0)
    write(filename, RATE, frames)