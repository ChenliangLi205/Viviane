import wave
import numpy as np
import matplotlib.pyplot as plt

# wav文件所在位置，这个是我电脑上的，请按照以下格式修改为自己的地址和文件名
defaultpath = r'G:\project\resource\music\piano WAV\16-C  -大字组.wav'


# 读取wav文件,提取声音数据
def readwav(path):
    with wave.open(path, 'rb') as f:
        par = f.getparams()  # 获取wav文件的参数
        framerate, framenum = par[2], par[3]  # 分别为帧率和帧数
        content = f.readframes(framenum)  # 获得全部帧的数据，得到的是bytes类型
        data = np.fromstring(content, dtype=np.int16)  # 将bytes类型转换为有符号16位整数数类型
        data.shape = -1, 2  # 生成一个两列的矩阵，一行就是一帧的数据
        data = data.T  # 转置矩阵，变成两行，各行分别为左、右声道
        time = np.arange(0, framenum) * (1.0 / framerate)  # 时间轴
        return data, time


# 绘制波形图
def display(x, y):
    plt.subplot(211)
    plt.plot(x, y[0], color='green')
    plt.subplot(212)
    plt.plot(x, y[1], color='blue')
    plt.show()


if __name__ == '__main__':
    filepath = input('请在代码中修改wav文件地址，若已修改则直接回车') or defaultpath
    try:
        wavdata, wavtime = readwav(filepath)
        display(wavtime, wavdata)
    except FileNotFoundError:
        print('未找到文件，请修改文件地址')
