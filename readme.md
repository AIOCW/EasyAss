# 智能助手 Try Again

## 注意
  尽量先看完整个介绍再动手，过些天会有相关的制作过程的教学
  视频上传，目前还未处理完。
  
  [本项目制作的视频教程](https://www.bilibili.com/video/av61588252)

## 效果

请看视频教程第六集

## 思路
### 唤醒模块

使用snowboy。

1. 唤醒模块一旦唤醒，暂时就不工作。直到该次唤醒工作结束后再
    继续工作
2. 唤醒之后，我们检查网络状态

### 录音模块

PyAudio

1. 10s之内没有人说话就自动关闭
    
    系统继续进入等待唤醒状态
    
2. 10s之后如果唤醒人继续在讲话，那么我们需要继续录音
    
    如果录音长度超过30s，我们就暂停录音，提示你也太啰嗦了
    否则我们就正常的进入下一步
    
3. 录制完成的音频,存储成wav，流处理的方式直接进行stt处理

    录音完成之后我们的录音模块暂时就停止工作

### 语音转文字stt

Baidu stt

1. 将使用百度的python的stt
2. 返回文字，我们接收文字。
3. 如果我们返回文字是空的或者其他的错误，我们提示您能再说
    一遍吗，我没听清楚（自动进入录音状态）。出错后跟出错
    提示，做出相应的反馈，网络错误（进入待唤醒状态）

### 对话机器人

tuling123.com的对话机器人

1. 我们免费对话机器人
2. 需要上传我们文字
3. 返回他的答案
4. 返回出错，处理方式同上

### 文字转语音模块tts

百度tts模块

1. 将对话机器人，返回文字转换成语音
2. 返回语音如果出错，我们处理同上

### 播放模块

PyAudio

1. 将这个语音播放出来

### 主体控制模块

1. 当对话机器人回应唤醒人的时候，是否自动进入下一轮的录音
    或者，是回应完之后就进入待唤醒状态。
2. 如果加入只能家具控制，那么我们需要两种方式来做

    a. 我们从这个stt返回后的语句中查询对应的关键字，然后
        处理。
    b. 使用其他的唤醒词，Again Try。
 
### nlp的意图匹配模块

示例：

我说：帮我把灯打开

系统（明白是我要打开我的灯，而不是和它聊天）：打开灯

我不想聊了

系统要退出循环聊天




## 开始手动配置

### 唤醒模块

1.配置snowboy的编译环境

    sudo apt-get install python-pyaudio python3-pyaudio sox
    
    sudo pip install pyaudio
    
    sudo pip3 install pyaudio
    
    cd 你的项目根目录/
    
    mkdir SBCompile
    
    wget http://downloads.sourceforge.net/swig/swig-3.0.10.tar.gz
    
    sudo apt-get install libpcre3 libpcre3-dev
    
    ls
    
    tar -zxvf swig-3.0.10.tar.gz
    
    cd swig-3.0.10/
    
    ./configure --prefix=/usr --without-clisp --without-maximum-compile-warnings && make
    
    sudo make install
    
    sudo install -v -m755 -d /usr/share/doc/swig-3.0.10
    
    sudo cp -v -R Doc/* /usr/share/doc/swig-3.0.10
    
    sudo apt-get install libatlas-base-dev
    
    cd ..
    
    mkdir rec_voice
    
    cd rec_voice/
    
    ls
    
    rec 1.wav
    
    ls
    
编译snowboy的准备工作结束

    cd ..
    
    git clone https://github.com/Kitt-AI/snowboy.git
    
    （这个是我没看明白，下面这句不用执行，把视频看下去就知道了）
    sudo apt-get install libmagic-dev libatlas-base-dev
    
    cd snowboy/
    
    cd swig/
    
    cd Python/
    
    make
    
    cd ..
    
    cd Python3/
    
    make
    
    exit
    
### 语音识别模块

    sudo pip3 install baidu-aip
    
    exit

### 对话模块

主要是代码
    
### 语音合成模块

与语音识别模块一直，主要是写几个代码

### 语音播放模块

    sudo pip3 install playsound

## 运行

需要更新stt_tts下的appid ak sk，理论上就可以在hotword下
的try_again_detect.py直接运行就行。实际上可能需要安装一些库
大家最好就是看看上面的过程。默认的唤醒词是smart mirror

本项目主要的目的在于给大家一个手动制作一个智能音箱的示例
如果真的想要实用，建议使用本文最后的
[Wukong](https://github.com/wzpan/wukong-robot)项目

本项目还有对应的教学视频，目前还未对一些秘钥进行打码，所以暂未
上传，之后将免费给大家。


## 相关物

[百度语音技术](https://ai.baidu.com/tech/speech/asr)

[Snowboy](https://snowboy.kitt.ai)

[Tuling123代码源](https://github.com/littlecodersh/EasierLife/blob/master/Plugins/Tuling/tuling.py)

[Tuling123官网](http://www.turingapi.com/)

[emotibot](http://botfactory.emotibot.com/)

[Wukong](https://github.com/wzpan/wukong-robot)

[百度的对话机器人](https://ai.baidu.com/docs#/UNIT-v2-service-API/top)