# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 21:01:56 2019
@author: 齐用卡
"""
import csv
import threading
import os
import pandas as pd
import numpy as np
from scipy.fftpack import fft
import glob

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True

def file_num(path):
    input = path + '/' +'*csv'
    files=glob.glob(input)
    num=len(files)
    return num
fft_size = 125000           #FFT处理的取样长度
sampling_rate = 1250000     #采样率

path = '/home/qyk/Desktop/电抗器'
foldernames = os.listdir(path + '/'+'dataset')
foldernames.sort()
print(foldernames)
for folder in range(len(foldernames)):
    input_path = '/home/qyk/Desktop/电抗器' + '/'+'dataset' + '/'+foldernames[folder]
    output_path = '/home/qyk/Desktop/电抗器' + '/'+'output' + '/'+foldernames[folder]
    mkdir(output_path)
    filenames = os.listdir(input_path)   
    filenames.sort()

    index_array = 0     #索引
    data = np.array([0]*125000) #data

    for i in range(len(filenames)):
        input_file = input_path +'/'+ filenames[i]
        print(input_file)
        output_file = output_path +'/' +foldernames[folder]+'.csv'
        filename = filenames[i]
        if filename[-4:] == '.CSV' or filename[-4:] == '.csv':
            temp = pd.read_csv(input_file, sep = ',', header=14,engine = 'c')
            keys = list(temp)
            index = keys[1]
            CH1 = temp[index]
            CH1_index = filename.split('.')[0]
            length = len(CH1)
            if length <125000:
                for ii in range(length,125000):
                    CH1[ii]=0
            data = np.vstack((data,CH1))
            index_array = np.vstack((index_array,CH1_index))
    excel = np.hstack((index_array,data))
    excel = excel[1:len(filenames)]

    print(excel.shape[0],excel.shape[1])

    csvFile = open(output_file, "w",newline='')            #创建csv文件
    writer = csv.writer(csvFile)                  #创建写的对象

    writer.writerows(excel)
    csvFile.close()



































'''
index_array = 0
row =0 
for i in range (len(filenames)):
    file = filenames[i]
    if file[-4:] =='.csv' or file[-4:] =='.CSV':
        filename = file[:-4]

        x =np.arange(0,0.1,1/sampling_rate)         #时间序列横坐标
        x= x[0:int(fft_size)]
        data_y = np.array(data[row:row+1])
        y = data_y[0]
        y = y[1:int(fft_size+1)]
            
        fft_y=fft(y) 
        fft_y=np.abs(fft_y)
            
        #freq = np.linspace(0, sampling_rate/2, fft_size/2+1)                # 频率个数
        array = np.array([0]*11)
            
        #print(array)
        ii=0
        for point in range(0,110,10):          
            #m = freq[int(point)]
            n = fft_y[int(point)]
            array[ii] = n
            ii+=1
        row = row + 1
        excel = np.vstack((excel,array))        
        index_array = np.vstack((index_array,filename))
        
print(excel)
print("------------------------------------------------")
print(index_array)
print("------------------------------------------------")
csvFile = open(output_path, "w",newline='')            #创建csv文件
writer = csv.writer(csvFile)                  #创建写的对象
                             
#writer.writerow(["index","0Hz","100Hz","200Hz","300Hz","400Hz","500Hz","600Hz","700Hz","800Hz","900Hz","1000Hz"])     #写入列的名称
excel = np.hstack((index_array[1:38],excel[1:38]))
writer.writerows(excel)
csvFile.close()
'''