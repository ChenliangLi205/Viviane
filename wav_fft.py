import matplotlib.pyplot as plt 
import numpy as np
import wave


def show(ori_func, rate):
    n = len(ori_func)
    interval = 1. / rate
    ft = np.fft.fft(ori_func)

    # 绘制原始函数
    plt.subplot(2, 1, 1) 
    plt.plot(np.arange(0, n) * interval, ori_func, color='black')
    plt.xlabel('Time'), plt.ylabel('Amplitude')

    # 绘制变换后的函数
    plt.subplot(2, 1, 2)
    frequency = np.arange(n / 2) / (n * interval)
    nfft = abs(ft[range(int(n / 2))] / n)
    print(len(nfft))
    plt.plot(frequency, nfft, color='red')
    plt.xlabel('Freq (Hz)'), plt.ylabel('Amp. Spectrum')

    plt.show()


def readwav(path):
    # 读wav文件，返回波形数据（1维数组）和帧率（整数）
    with wave.open(path, 'rb') as f:
        par = f.getparams()
        framerate, framenum = par[2], par[3]
        content = f.readframes(framenum)
        data = np.fromstring(content, dtype=np.int16)
        data.shape = -1, 2
        data = data.T
        data = data[0]  # 取单声道（0为左声道，1为右声道）
        return data, framerate


def segment(data, span=4000):
    # 传入整个乐曲的波形数据（1维数组），返回一个由分段组成的2维数组
    # 每个分段都是长度固定为span的1维数组，并且仍是波形数据
    # 注意span的单位是帧，不是毫秒，转换为时间单位需要除以帧率
    # 由于data的长度不一定是span的整数倍，需要在data末尾用0填充至整数倍，以保证最后一个分段的长度仍为span
    n = len(data)
    if n % span:
        lack = span - n % span
        complete = np.concatenate((data, np.zeros(lack, dtype=np.int16)))
    else:
        complete = data.copy()
    return complete.reshape(-1, span)


if __name__ == '__main__':
    wavdata, wavrate = readwav(r'28-C.wav')
    seg = segment(wavdata)
    show(seg[0], wavrate)
    show(seg[1], wavrate)
