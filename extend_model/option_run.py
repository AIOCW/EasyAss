import time
from extend_model.music import Music

music_state = False

def play_music(option):
    music_player = Music()
    global music_state
    if music_state:
        if option == "暂停":
            music_player.stop()
        if option == "继续":
            music_player.start()
        if option == "下一个":
            music_player.next()
        if option == "上一个":
            music_player.last()
        if option == "增加音量":
            music_player.set_volume(40)
        if option == "减少音量":
            music_player.set_volume(20)
        if option == "退出":
            music_player.exit()
            music_state = False
        print(music_player.now_playing_music_name())
    else:
        if option == "播放":
            music_player.play()
            music_player.set_volume(20)
            music_state = True



def execute_option(device_result):
    if device_result["device"] == "音乐":
        play_music(device_result["option"])


