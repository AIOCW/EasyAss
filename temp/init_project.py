from stt_tts.baidu_tts_wav import text_to_speak
def generate_local_tips():
    local_sentences = ['net_error: 网络连接，错误请稍后重试，或检查网络连接。',
                       'no_speak: 你喊我咋啥也不说呢。',
                       'stop_speak: 你怎么突然不说话了呢，那我也不理你了。',
                       'speak_bye: 那拜拜咯！下回再聊，我会想你的。',
                       'speak_ok: 好的，马上执行该操作。',
                       'speak_shutdown: 请注意，系统正在关闭中，请稍后。关闭后无法语音唤醒，需要手动执行。'
                      ]
    for sentence in local_sentences:
        key_value = sentence.split(": ")
        key = key_value[0]
        value = key_value[1]
        # print(key, value)
        text_to_speak(value, save_filename='../temp/'+key+'.wav')
        print("success get {}".format(key))


if __name__ == "__main__":
    generate_local_tips()