from hotword import snowboydecoder
import threading
import time

THIS_PATH = "/home/yaque/Ass/hotword/"
interrupted = False


class SmartMirrorDetectThread(threading.Thread):
    queueLock = threading.Lock()

    def __init__(self, communicate_queue, t_name):
        threading.Thread.__init__(self)
        self.communicate_queue = communicate_queue

        self.model = THIS_PATH + "resources/models/smart_mirror.umdl"

    def run(self):
        # capture SIGINT signal, e.g., Ctrl+C
        # signal.signal(signal.SIGINT, self.signal_handler)

        detector = snowboydecoder.HotwordDetector(self.model, sensitivity=0.38)
        # print('Listening... Press Ctrl+C to exit')

        # main loop
        detector.start(detected_callback=self.detected_callback,
                       audio_recorder_callback=self.audio_recorder_callback,
                       interrupt_check=self.interrupt_callback,
                       sleep_time=0.01)

        detector.terminate()

    def audio_recorder_callback(self, fname):
        self.queueLock.acquire()
        self.communicate_queue.put(fname)
        self.queueLock.release()
        print("send end")
        while True:
            self.queueLock.acquire()
            if not self.communicate_queue.empty():
                flag_m = self.communicate_queue.get()
                self.queueLock.release()
                print(flag_m)
                break
            else:
                self.queueLock.release()
                continue
        return flag_m

    def detected_callback(self):
        snowboydecoder.play_audio_file()
        print('recording audio...', end='', flush=True)

    def stop(self):
        global interrupted
        interrupted = True

    def interrupt_callback(self):
        global interrupted
        return interrupted




