import matplotlib.pyplot as plt 
import numpy as np
import wave


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


def fft(ori_func, rate):
    # 传入波形数据（1维数组）和帧率（整数），进行傅里叶变换处理
    # 返回的frequency为频谱图的x值的序列，nfft为y值的序列，两者一一对应，均为1维数组
    # 传入的rate参数对于傅里叶变换的计算是无关的，只是决定了nfft的每个值对应的频率（即确定x轴的单位长度）
    n = len(ori_func)
    ft = np.fft.fft(ori_func)
    nfft = abs(ft[range(int(n / 2))] / n)
    frequency = np.arange(n / 2) / (n / rate)
    return nfft, frequency


if __name__ == '__main__':
    wavdata, wavrate = readwav(r'28-C.wav')
    seg = segment(wavdata)

    m = len(seg)
    for i in range(m):
        x = seg[i]
        interval = 1. / wavrate

        plt.subplot(m, 2, 2 * i + 1)
        plt.plot(np.arange(0, len(x)) * interval, x, color='black')
        plt.xlabel('Time'), plt.ylabel('Amplitude')

        plt.subplot(m, 2, 2 * i + 2)
        spec, freq = fft(x, wavrate)
        plt.plot(freq, spec, color='red')
        plt.xlabel('Freq (Hz)'), plt.ylabel('Amp. Spectrum')

    plt.show()
