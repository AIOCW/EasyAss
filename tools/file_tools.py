import os
import json
import struct
import traceback
import time

from tools.md5 import getmd5
from tools.net_tools import data2byte, unpackage_data_2_security, package_data_2_security, byte2data


def get_file_inform(file_path, send_aim):
    # 封装文件信息
    try:
        filesize_bytes = os.path.getsize(file_path)
        md5 = getmd5(file_path)
        head_dir = {
            'filename': file_path.split("/")[-1],
            'filesize': filesize_bytes,
            'filepath': 'file/',
            'aim_device': send_aim,
            'md5': md5
        }
        head_info = json.dumps(head_dir)
        return head_info
    except Exception as e:
        print(e.args)
        print(traceback.format_exc())
        print("文件封装错误")
        return 0, head_info, 0

# 测试专用函数
def read_file_test(file_path = "test.txt"):
    s = time.time()
    counter = 0
    with open(file_path, 'rb') as sf:
        while True:
            data = sf.read(1024)
            data_len = len(data)
            if data_len == 0:
                break
            elif data_len == 1024:
                data = data + data2byte(counter)
            elif data_len < 1024:
                for i in range(data_len, 1024):
                    data += b'0'
                data = data + data2byte(counter)
            print(data)
            print(len(data))
            print(counter)
            counter += 1
                # break
    print(time.time() - s)


def split_file(split_file_path, split_number):
    temp_file_list = []
    with open(split_file_path, 'rb') as sf:
        file_size = os.path.getsize(split_file_path)
        split_length = file_size / split_number
        for i in range(0, split_number):
            one_file_size = 0
            temp_file_list.append("TempFile/" + str(i) + ".elt")
            with open("TempFile/" + str(i) + ".elt", 'wb') as slf:
                while True:
                    data = sf.read(1024)
                    one_file_size += len(data)
                    slf.write(data)
                    if len(data) < 1024:
                        break
                    elif one_file_size > split_length:
                        break
                    # break
    return temp_file_list


def composite_file(temp_file_path, file_path):
    with open(file_path, 'wb') as save_file:
        for root, dir, files in os.walk(temp_file_path):
            for file in files:
                with open(root + file, 'rb') as file_read:
                    save_file.write(file_read.read())
                os.remove(root + file)
    pass

if __name__ == "__main__":
    # read_file_test()
    split_file("java.exe", 5)
    composite_file("../TempFile/", "a.apk")
    getmd5("a.apk")
    getmd5("java.exe")
