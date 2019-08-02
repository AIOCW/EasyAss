from hotword import snowboydecoder
import signal
import os

from stt_tts.baidu import rec_speak_to_text, text_to_speak
from tuling.tuling123 import get_response
from tuling.baidu_robot import get_result

from mouth.play import play_audio_file_playsound
from mouth.play import play_audio_file_change_to_mp3
from mouth.play import play_audio_file_pygame

interrupted = False
session_id = ""
stop_key_words = ['不聊了', '你歇着吧', '我走了', '我不想聊了']


def audioRecorderCallback(fname):
    global session_id
    flag_m = 0
    print("converting audio to text")
    sentence = rec_speak_to_text(fname)
    if isinstance(sentence, int):
        if sentence == 1:
            robot_answer_fname = text_to_speak("网络错误，请稍后重试。")
        elif sentence == 0:
            if session_id == "":
                robot_answer_fname = text_to_speak("你喊我咋啥也不说呢。")
            else:
                robot_answer_fname = text_to_speak("你怎么突然不说话了呢，那我也不理你了。")
                session_id = ""
    else:
        flag_end = 0
        for one_stop_key_word in stop_key_words:
            if one_stop_key_word in sentence:
                flag_end = 1
                break
        if flag_end == 1:
            robot_answer_fname = text_to_speak("那拜拜咯！下回再聊，你早找我哦，我会想你的。")
            session_id = ""
        else:
            # robot_answer = get_response(sentence)
            robot_answer, session_id = get_result(sentence, session_id)
            robot_answer_fname = text_to_speak(robot_answer)
            flag_m = 1
    play_audio_file_pygame(robot_answer_fname)
    # print(fname)
    # print(robot_answer_fname)
    os.remove(fname)
    os.remove(robot_answer_fname)

    return flag_m



def detectedCallback():
    snowboydecoder.play_audio_file()
    print('recording audio...', end='', flush=True)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

# if len(sys.argv) == 1:
#     print("Error: need to specify model name")
#     print("Usage: python demo.py your.model")
#     sys.exit(-1)

# model = sys.argv[1]
model = "resources/models/smart_mirror.umdl"

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.38)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)

detector.terminate()




