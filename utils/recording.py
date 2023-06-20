import pyaudio
import soundfile as sf
import numpy as np
import sounddevice # needed to suppres linux error messsages in terminal
import time

def record_audio(filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050  # samples per second
    THRESHOLD = 1000  # Adjust this value to set the sensitivity of the voice detection
    SILENCE_LIMIT = 1.1  # Number of seconds of silence before stopping the recording
    TIMEOUT_AFTER_SECONDS = 10  # Maximum recording time in seconds
    IS_TIMEOUT = False
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Wait for the user to start speaking
    start_time = time.time()
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        if np.abs(data).mean() > THRESHOLD:  # check mean amplitude of the chunk
            break
        if (time.time() - start_time) >= TIMEOUT_AFTER_SECONDS:
            IS_TIMEOUT = True
            break

    # Record for the specified duration or until the user stops speaking
    frames = []
    silent_frames = 0
    
    start_time = time.time()
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
    sf.write(filename, frames, RATE)

    if IS_TIMEOUT:
        return True
    else:
        return False