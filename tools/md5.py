'''
Python 获取文件的MD5值
getMd5.py
'''
import os
import string
import hashlib


def getmd5(file):
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            m.update(line)
    md5code = m.hexdigest()
    print(md5code)
    return md5code


def getdisklist():
    disklist = []
    d = string.ascii_uppercase
    # print(d)
    for w in d:
        disk = w + ':'
        if os.path.isdir(disk):
            disklist.append(disk)
    # print(disklist)
    return disklist


def scan(disklist):
    # print(disklist)
    for disk in disklist:
        # print(disk)
        os.chdir(disk + '/')
        tree = os.walk('/')
        for dir in tree:
            for file in dir[2]:
                if '.jpg' in file or '.pdf' in file or '.com' in file or '.exe' in file or '.dll' in file:
                    myfile = disk + dir[0] + '/' + file
                    print(myfile)
                    mymd5code = getmd5(myfile)
                    with open('md5.txt', 'a') as f:
                        f.write(myfile + '\n' + mymd5code + '\n')
                    print('md5: ', mymd5code)


if __name__ == '__main__':
    # 0e15d65926c9cebd115a0e139c235c25
    # 0e15d65926c9cebd115a0e139c235c25
    getmd5("../file/TestPackage.zip")