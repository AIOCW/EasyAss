from playsound import playsound
from pydub import AudioSegment
import pyaudio
import wave
import os
import time
import pygame

CHUNK = 1024


def play_audio_file_playsound(fname):
    playsound(fname)


def play_audio_file_pygame(fname):
    pygame.mixer.init()
    pygame.mixer.music.load(fname)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


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


def play_audio_file_change_to_mp3(fname):
    song = AudioSegment.from_mp3(fname)
    filename = '../temp/baidu' + str(int(time.time())) + '1.mp3'
    song.export(filename, format="wav")
    play_wave_pyaudio(filename)
    os.remove(filename)


if __name__ == "__main__":
    play_audio_file_playsound("../temp/baidu1564470005.mp3")