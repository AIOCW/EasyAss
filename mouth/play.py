import pyaudio
import wave
import os
import time

CHUNK = 1024



def play_wave_pyaudio(filename):
    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == "__main__":
    play_wave_pyaudio("../temp/net_error.wav")