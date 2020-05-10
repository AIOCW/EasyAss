from aip import AipSpeech
import os

""" 你的 APPID AK SK """
APP_ID = '11684493'
API_KEY = 'XYShi1grKEeqssWISnhr3EupVLLliChi'
# SECRET_KEY = '***************************'
SECRET_KEY = '18XEgGeDdWfHKZ8lUbsZLynRzQOtwpSN'

# 由于公开的秘钥不好，所以不给
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


# 识别本地文件
def rec_speak_to_text(fname):
    result = 0
    try:
        sentence = client.asr(get_file_content(fname), 'wav', 16000, {
            'dev_pid': 1536,
        })
        # print(sentence)
        # 删除录音文件
        os.remove(fname)
        if sentence['err_no'] == 0:
            result_list = sentence['result']
            for i, one in enumerate(result_list):
                if i != 0:
                    result = result + "。" + one
                else:
                    result = one
    except:
        return 1

    return result


if __name__ == "__main__":
    s = rec_speak_to_text("../temp/output1564468756.wav")
    print(s)