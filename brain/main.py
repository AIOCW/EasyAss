import sys
# # sys.path.append("你的Ass的目录")
sys.path.append("/home/yaque/Ass")
# print(sys.path)
# 以上代码仅需在树莓派环境部署时使用.
# update==使用start.sh脚本时使用
import queue
import threading
import time
import os
from hotword.smart_mirror_detect_thread import SmartMirrorDetectThread

from stt_tts.baidu import rec_speak_to_text
from stt_tts.baidu_tts_wav import text_to_speak
from tuling.baidu_robot import get_result

from brain.match import device_match,init_device_match

from extend_model.option_run import execute_option
from extend_model.control import ControlThread

# 以下播放方式
"""
在几种播放方式中
wave_pyaudio 这个只能播放wav格式文件，配合最新的百度tts使用，该种方式树莓派系统和Ubuntu系统都支持
"""
from mouth.play import play_wave_pyaudio


BASE_PATH = "/home/yaque/Ass/"
stop_key_words = ['不聊了', '你歇着吧', '我走了', '我不想聊了', '系统关闭']

queueLock = threading.Lock()

communicate_queue = queue.Queue(10)

init_device_match()

control_thread = ControlThread("control")
control_thread.start()

smart_mirror_detect_thread = SmartMirrorDetectThread(communicate_queue, "hotword_detect")
smart_mirror_detect_thread.start()
session_id = ""
out_and_end = 0
while True:
    fname = ""
    queueLock.acquire()
    if not communicate_queue.empty():
        fname = communicate_queue.get()
        print("传送来的数据是{}".format(fname))
    queueLock.release()
    if fname == "":
        continue
    flag_m = 0
    print("converting audio to text")
    sentence = rec_speak_to_text(fname)
    if isinstance(sentence, int):
        if sentence == 1:
            play_wave_pyaudio(BASE_PATH + 'temp/net_error.wav')
        elif sentence == 0:
            if session_id == "":
                play_wave_pyaudio(BASE_PATH + 'temp/no_speak.wav')
            else:
                play_wave_pyaudio(BASE_PATH + 'temp/stop_speak.wav')
                session_id = ""
    else:
        print(sentence)
        flag_end = 0
        for one_stop_key_word in stop_key_words:
            if one_stop_key_word in sentence:
                if one_stop_key_word == '系统关闭':
                    flag_end = 2
                else:
                    flag_end = 1
                break
        if flag_end == 1:
            play_wave_pyaudio(BASE_PATH + 'temp/speak_bye.wav')
            session_id = ""
        elif flag_end == 2:
            play_wave_pyaudio(BASE_PATH + 'temp/speak_shutdown.wav')
            session_id = ""
            out_and_end = 1

        else:
            devices_m_result = device_match(sentence)
            if devices_m_result["right"] == 2:
                play_wave_pyaudio(BASE_PATH + 'temp/speak_ok.wav')
                execute_option(devices_m_result)
            else:
                robot_answer, session_id = get_result(sentence, session_id)
                robot_answer_fname = text_to_speak(robot_answer)
                flag_m = 1
                play_wave_pyaudio(robot_answer_fname)
                os.remove(robot_answer_fname)
    queueLock.acquire()
    if not communicate_queue.full():
        communicate_queue.put(flag_m)
    queueLock.release()
    time.sleep(1)
    if out_and_end == 1:
        print("break")
        break

print("close children program")
smart_mirror_detect_thread.stop()
print("系统关闭")
