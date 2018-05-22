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
    with wave.open(path, 'rb') as f:
        par = f.getparams()
        framerate, framenum = par[2], par[3]
        content = f.readframes(framenum)
        data = np.fromstring(content, dtype=np.int16)
        data.shape = -1, 2
        data = data[2200:4200]  # 截取其中2000帧
        data = data.T
        data = data[0]  # 只取左声道
        return data, framerate


if __name__ == '__main__':
    wavdata, wavrate = readwav(r'28-C.wav')
    show(wavdata, wavrate)
