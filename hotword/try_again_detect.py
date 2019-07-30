from hotword import snowboydecoder
import signal
import os

from stt_tts.baidu import rec_speak_to_text, text_to_speak
from tuling.tuling123 import get_response
from tuling.baidu_robot import get_result
# from mouth.play import play_audio_file
from playsound import playsound

interrupted = False


def audioRecorderCallback(fname):
    print("converting audio to text")
    print(fname)
    sentence = rec_speak_to_text(fname)
    # robot_answer = get_response(sentence)
    robot_answer, session_id = get_result(sentence, "")
    print(robot_answer)
    robot_answer_fname = text_to_speak(robot_answer)
    print(robot_answer_fname)
    playsound(robot_answer_fname)
    os.remove(fname)
    os.remove(robot_answer_fname)



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




