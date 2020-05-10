
import threading
import time
import socket
from socket import *
import json
import struct
import time
import traceback

from tools.net_tools import unpackage_data_2_security, package_data_2_security ,data2byte, byte2data
from stt_tts.baidu_tts_wav import text_to_speak
from mouth.play import play_wave_pyaudio

TAG = "tools_sockt_client:     "

THIS_PATH = "/home/yaque/Ass/extend_model/"
interrupted = False


class ControlThread(threading.Thread):
    # queueLock = threading.Lock()

    def __init__(self, t_name):
        threading.Thread.__init__(self)
        self.host = '192.168.100.18'
        self.port = 8080
        self.device_name = 'easybox'
        self.is_send_heartbeat = True  # 1
        self.send_code = -1
        self.recv_code = -1

        self.return_type_flag = ''
        self.send_aim = ''

        self.text_message_aim_device = ''
        self.text_message = ''

    def run(self):
        self.start_net_fun()
        while True:
            if self.is_connection:
                print("{}可以连接到服务器".format(TAG))
                # 心跳保持工具
                if self.is_send_heartbeat:
                    print('heartbeat')
                    self.heartbeat()
                    # self.my_signal.emit("2" + "+0~^D" + self.heartbeat())
                    time.sleep(3)
                    print("当前recv_code{}".format(self.recv_code))

                # 获取已连接服务端的客户端数量
                elif self.send_code == 1001:
                    self.tcp_client.send(package_data_2_security(data2byte(1001)))
                    confirm_code_buffer = self.tcp_client.recv(4)
                    confirm_code = byte2data(unpackage_data_2_security(confirm_code_buffer))
                    if confirm_code == 1001:
                        message_len_buffer = self.tcp_client.recv(4)
                        message_len = byte2data(unpackage_data_2_security(message_len_buffer))
                        message_buffer = self.tcp_client.recv(message_len)
                        message = unpackage_data_2_security(message_buffer)
                        self.tcp_client.send(package_data_2_security(data2byte(1001)))
                        message = self.return_type_flag + "1001" + "+0~^D" + message.decode('utf-8')

                        self.send_code = -1
                        self.is_send_heartbeat = True
                    else:
                        print("获取数据失败")
                    print("end 1001================")

                # 发送文本消息
                elif self.send_code == 1011:
                    self.send_text_message()

                # 文件发送完成
                elif self.send_code == 1100:
                    self.send_file_finish()

                # 接收
                # 接收文本
                elif self.recv_code == 91011:
                    self.rece_text_message()



    def rece_text_message(self):
        confirm_code_buffer = self.tcp_client.recv(4)
        confirm_code = byte2data(unpackage_data_2_security(confirm_code_buffer))
        if confirm_code == 1011:
            json_data_len_buffer = self.tcp_client.recv(4)
            json_data_len = byte2data(unpackage_data_2_security(json_data_len_buffer))
            json_data_buffer = self.tcp_client.recv(json_data_len)
            json_data = unpackage_data_2_security(json_data_buffer)
            json_data = json_data.decode('utf-8')
            json_data = json.loads(json_data)

            text_message = "91011" + "+0~^D" + json_data['security_md5_text']
            play_wave_pyaudio(text_to_speak(json_data['security_md5_text']))

            self.recv_code = -1
            self.is_send_heartbeat = True
    # 心跳处理段
    def heartbeat(self):
        print("进入心跳包发送阶段")
        success_code = 0
        try:
            self.tcp_client.send(package_data_2_security(data2byte(1010)))
            success_code_buffer = self.tcp_client.recv(4)
            success_code = byte2data(unpackage_data_2_security(success_code_buffer))
            if success_code == 1010:
                print("心跳包接收的是{}".format(success_code))
        except ValueError:
            print("值错误{}，进行服务重连或服务切换".format(ValueError))
            self.is_connection = False
        except Exception as e:
            print(e.args)
            print("==============")
            print(traceback.format_exc())
            print("{}".format("心跳保持出现问题，进行服务重连或切换"))
            self.is_connection = False
        if success_code == 1010:
            status = '在线9'
        elif success_code == 91011:
            status = '有文本信息'
            self.recv_code = 91011
            self.is_send_heartbeat = False
            return status
        elif success_code == 91100:
            status = '文件接收中。。。'
            self.recv_code = 91100
            self.is_send_heartbeat = False
            return status
        elif success_code == 9110040:
            status = '在线9'
            print("服务器成功接收发送的大文件，服务器计算md5值相同")
            tip_message = "91100" + "+0~^D" + "文件发送成功"
        elif success_code == 110041:
            status = '接收大文件。。'
            self.is_send_heartbeat = False
            self.recv_code = 110041
            return status
        else:
            status = '下线'
        return status

    # 开始连接服务器段
    def start_net_fun(self):
        print(self.host, self.port)
        self.tcp_client = socket(AF_INET, SOCK_STREAM)
        ip_port = ((self.host, int(self.port)))
        self.tcp_client.connect_ex(ip_port)
        try:
            print('向服务端发送本机信息')
            json_message = {
                'client_name': self.device_name
            }
            json_message = json.dumps(json_message)
            json_message_buffer = json_message.encode('utf-8')
            json_message_buffer = package_data_2_security(json_message_buffer)

            self.tcp_client.send(package_data_2_security(data2byte(1000)))
            json_message_len_buffer = data2byte(len(json_message_buffer))
            json_message_len_buffer = package_data_2_security(json_message_len_buffer)
            self.tcp_client.send(json_message_len_buffer)  # 这里是4个字节
            self.tcp_client.send(json_message_buffer)  # 发送报头的内容
            success_code_buffer = self.tcp_client.recv(4)
            success_code = byte2data(unpackage_data_2_security(success_code_buffer))
            if success_code == 1000:
                self.is_connection = True
        except:
            self.is_connection = False
            print("Error{}, is_connection={}".format("网络错误，重置网络标识，启动服务器链接监测", self.is_connection))



