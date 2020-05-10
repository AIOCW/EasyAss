import sqlite3
import os
import pygame
import time
import threading

THIS_PATH = "/home/yaque/Ass/extend_model/"

class Music(object):

    def __init__(self):
        self.play_list = [""]
        self.play_list = self.select_play_list()
        self.total = len(self.play_list)
        pygame.mixer.init()
        self.play_thread = None
        self.is_playing = True
        self.play_number = 0

    def player(self):
        while self.is_playing:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.play_list[self.play_number])
                pygame.mixer.music.play(self.play_ways())
            else:
                time.sleep(0.3)

    def play(self):
        self.play_thread = threading.Thread(target=self.player)
        self.play_thread.start()

    def start(self):
        self.is_playing = True
        pygame.mixer.music.unpause()

    def stop(self):
        self.is_playing = False
        pygame.mixer.music.pause()

    def exit(self):
        self.is_playing = False
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass

    def next(self):
        self.is_playing = False
        pygame.mixer.music.stop()
        # pygame.mixer.quit()
        if self.play_number < self.total - 1:
            self.play_number += 1
        else:
            self.play_number = 0
        self.is_playing = True
        self.play()

    def last(self):
        self.is_playing = False
        pygame.mixer.music.stop()
        # pygame.mixer.quit()
        if self.play_number == 0:
            self.play_number = self.total - 1
        else:
            self.play_number -= 1
        self.is_playing = True
        self.play()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume / 100)

    def now_playing_music_name(self):
        return self.play_list[self.play_number]

    def select_play_list(self):
        musics = [THIS_PATH + "Beat_It(Single_Version)-Michael_Jackson-551465 (big).mp3"]
        return musics

    def play_list_create(self):
        pass

    def play_list_add(self):
        pass

    def play_list_delete(self):
        pass

    def play_list_search(self):
        pass

    def play_ways(self, ways_number=-1):
        if ways_number == -1:
            ways_number = 1
        return ways_number


if __name__ == "__main__":
    music_player = Music()
    music_player.play()
    print("start")
    time.sleep(1)
    music_player.stop()
    print("stop")
    time.sleep(5)
    music_player.start()
    print("start")
    time.sleep(10)
    music_player.next()
    print("next")
    time.sleep(5)
    music_player.last()
    print("last")
    time.sleep(1)
    music_player.set_volume(10)
    print("set_volume")
    time.sleep(10)
    music_player.set_volume(80)
    print("set_volume")
    time.sleep(10)
    print(music_player.now_playing_music_name())
    music_player.exit()
    print("end")

