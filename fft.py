# -*- coding: utf-8 -*-
"""
将数据读出来一行一行的进行fft，并且存起来
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
count = 0
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
foldernames = os.listdir(path + '/'+'output')
foldernames.sort()
#print(foldernames)
for folder in range(len(foldernames)):
    index_array = 0     #索引
    data = np.array([0]*125000) #data

    count = count +1
    print("count:",count)
    input_path = '/home/qyk/Desktop/电抗器' + '/'+'output' + '/'+foldernames[folder]
    output_path = '/home/qyk/Desktop/电抗器' + '/'+'output' + '/'+foldernames[folder]
    print("input_path:",input_path)
    print("output_path:",output_path)

    mkdir(output_path)
    filenames = os.listdir(input_path)   
    filenames.sort()



    input_file = input_path +'/'+ foldernames[folder]+'.csv'
    output_file = output_path +'/' +foldernames[folder] + '_10fft.csv'
    print("input_file:",input_file)
    print("output_file:",output_file)

    
    temp = pd.read_csv(input_file, sep = ',', header=None,engine = 'c')
    samples = temp.shape[0]
    timestamp = temp.shape[1]
    print(samples,timestamp)
    for i in range(samples):
        index = temp[0][i]
        y =np.array(temp[i:i+1])
        y=y[0]
        y = y[1:]
        for chacter in range(len(y)):
            if y[chacter] == '-':
                y[chacter]=0
        y = fft(y) 
        y = np.abs(y)
        data = np.vstack((data,y))
        index_array = np.vstack((index_array,index))
        #print(data.shape[0],data.shape[1])
    print(index_array)
    index_array = index_array[1:]
    data = data[1:]
    excel = np.hstack((index_array,data))

    print(excel.shape[0],excel.shape[1])

    csvFile = open(output_file, "w",newline='')            #创建csv文件
    writer = csv.writer(csvFile)                  #创建写的对象
    writer.writerows(excel)
    csvFile.close()
