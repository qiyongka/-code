'''
对数据进行fft，并且取出基频和倍频点的数据进行做图
'''
import os
import math
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from scipy.fftpack import fft,ifft

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True


fft_size = 125000           #FFT处理的取样长度
sampling_rate = 1250000     #采样率
path = '/home/qyk/Desktop/电抗器/output'
name_path = '/home/qyk/Desktop/电抗器/dataset'
folder_filenames = os.listdir(path)
folder_filenames.sort()
folder = 18
path = '/home/qyk/Desktop/电抗器/output'
input_path = path + '/'+ folder_filenames[folder]
files_path =name_path+ '/'+folder_filenames[folder]
files =  os.listdir(files_path)
files.sort()
print(files)
output_path = path + '/'+ folder_filenames[folder]+'/'+ '10_fft'
mkdir(output_path)
print(input_path)
input_file = input_path +'/'+ folder_filenames[folder] +'.csv'
print(input_file)
data = pd.read_csv(input_file, sep = ',', header=None)
samples = data.shape[0]
timestamp = data.shape[1]
print(samples,timestamp)
print("read is over")

x =np.arange(0,0.1,1/sampling_rate)         #时间序列横坐标
x= x[0:int(fft_size)]
for i in range (samples):
    y = np.array(data[i:i+1])
    y = y[0]
    y = y[1:]

    fft_y=fft(y) 
    fft_y=np.abs(fft_y)

    freq = np.linspace(0, sampling_rate/2, fft_size/2+1)
    plt.figure(figsize=(11,5 ))
    plt.subplot(121)

    plt.plot(x,y)  
    plt.xlabel('Time /s')
    plt.ylabel('Voltage /v')
    plt.grid(1) 
    plt.title('Time series')

    plt.subplot(122)
        #plt.figure(figsize=(6, 4))
    plt.plot(freq[0:120],fft_y[0:120],'red')
    plt.xlabel('Freq /Hz')
    plt.ylabel('fft')
    plt.title('fft',)
    plt.grid(1)
    for point in range(0,110,10):
        m = freq[int(point)]
        n = fft_y[int(point)]
        if np.isnan(n):
            n=0
            print("gggggggggggggggggggggggggggggggggggggg")
        #print(freq[int(point)],fft_y[int(point)])
        print(m,n)
        plt.annotate("(%d,%d)" % (m,n), xy= (m,n),xytext=(m, n+25),arrowprops=dict(arrowstyle="->"))
        #plt.savefig(output_file) 
    filename = files[i * 2]
    filename = filename.split('.')[0]
    output_file = output_path + '/' + filename+'.png'
    plt.savefig(output_file)
        #plt.show()

















