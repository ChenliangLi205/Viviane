# 生成一个正弦波的wav文件
# 首先复习一下正弦函数y = A sin(ω x + φ) + b中各个参数的含义
# A：振幅，声波中决定音量大小
# ω：圆频率，决定最小正周期T = 2π/ω，与频率之间的换算为2πf = ω
# φ：初相，表示波形在x轴方向上的平移（左加右减）
# b：表示波形在y轴方向上的平移（上加下减）
# 可只设定振幅和频率，其他参数设为0即可

import wave
import numpy as np
import struct

# wav文件参数
# 压缩方式的两个参数只能取这两个值，请勿改动
channels = 2  # 声道数
width = 2  # 位深（Byte）
framerate = 44100  # 帧率（Hz）
duration = 2  # 文件长度（s）
framenum = framerate * duration  # 总帧数
comptype = 'NONE'  # 压缩方式（不压缩）
compname = 'not compressed'  # 压缩方式（不压缩）

# 正弦波参数
volum = 27000  # 振幅，决定音量
frequency = 256  # 频率，决定音高


# 生成正弦波
# 通过修改channel的公式也可以产生其他的波形，可以自行尝试
def genedata(fnum, frate, a, f):
    time = np.array(range(fnum)) / frate
    channel0 = a * np.sin(2 * np.pi * f * time)  # 左声道
    channel1 = channel0  # 右声道
    sample = []  # 一个list用于储存声音数据
    for i in range(framenum):  # 对每一帧进行数据的添加操作
        sample.append(struct.pack('h', int(channel0[i])))  # 添加左声道数据
        sample.append(struct.pack('h', int(channel1[i])))  # 添加右声道数据
    sample_str = b''.join(sample)  # 将list中的数据转化成一个字符串，便于写入
    return sample_str


# 创建wav文件，写入声音数据
def writewav(param, samples):
    with wave.open('256Hz.wav', 'w') as f:
        f.setparams(param)  # 设定wav文件参数
        f.writeframes(samples)  # 写入数据


if __name__ == '__main__':
    par = (channels, width, framerate, framenum, comptype, compname)
    data = genedata(framenum, framerate, volum, frequency)
    writewav(par, data)
