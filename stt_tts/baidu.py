from aip import AipSpeech
import time

""" 你的 APPID AK SK """
APP_ID = '11684493'
API_KEY = 'XYShi1grKEeqssWISnhr3EupVLLliChi'
SECRET_KEY = '***************************'

# 由于公开的秘钥不好，所以不给
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
def rec_speak_to_text(fname):
    result = None
    sentence = client.asr(get_file_content(fname), 'wav', 16000, {
        'dev_pid': 1536,
    })
    print(sentence)
    if sentence['err_no'] == 0:
        result_list = sentence['result']
        for i, one in enumerate(result_list):
            if i != 0:
                result = result + "。" + one
            else:
                result = one
    return result


def text_to_speak(sentence):
    result = client.synthesis(sentence, 'zh', 4, {
        'vol': 5,
    })
    filename = '../temp/baidu' + str(int(time.time())) + '.mp3'
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(filename, 'wb') as f:
            f.write(result)
    return filename


if __name__ == "__main__":
    # s = rec_speak_to_text("../temp/output1564468756.wav")
    # print(s)
    text_to_speak("你好，百度。我吃了你。")