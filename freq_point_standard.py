# -*- coding: utf-8 -*-
"""
将fft就可以得到基频点和倍频点的增益，读取出来，并且做到归一化，并且存储起来
Created on Tue 10. 13 21:01:56 2019
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

path = '/home/qyk/Desktop/电抗器'
foldernames = os.listdir(path + '/'+'output')
foldernames.sort()
#print(foldernames)
for folder in range(len(foldernames)):
    index_array = 0     #索引
    data = np.array([0.0]*11) #data
    array =np.array([0.0]*11)

    count = count +1
    print("count:",count)
    input_path = '/home/qyk/Desktop/电抗器' + '/'+'output' + '/'+foldernames[folder]
    output_path = '/home/qyk/Desktop/电抗器' + '/'+'output' + '/'+foldernames[folder]
    print("input_path:",input_path)
    print("output_path:",output_path)

    mkdir(output_path)
    filenames = os.listdir(input_path)   
    filenames.sort()

    input_file = input_path +'/'+ foldernames[folder]+'_fft_point.csv'          #输入fft后的结果
    output_file = output_path +'/' +foldernames[folder] + '_fft_point_standard.csv'  #输出基频和倍频的增益
    print("input_file:",input_file)
    print("output_file:",output_file)

    
    temp = pd.read_csv(input_file, sep = ',', header=0,engine = 'c')
    temp = np.array(temp)
    samples = temp.shape[0]
    timestamp = temp.shape[1]
    print(samples,timestamp)
    print(temp)

    for i in range(samples):
        index = temp[i][0]
        print(index)
        y =np.array(temp[i:i+1])
        y=y[0]
        y = y[1:]

        for chacter in range(len(y)):
            if y[chacter] == '-':
                y[chacter]=0
        for point in range(11):          
            #m = freq[int(point)]
            array[int(point)] = y[int(point)] / y[1]
        print(array)
        data = np.vstack((data,array))
        index_array = np.vstack((index_array,index))
     
    print(index_array)
    index_array = index_array[1:]
    data = data[1:]
    excel = np.hstack((index_array,data))

    print(excel.shape[0],excel.shape[1])

    csvFile = open(output_file, "w",newline='')            #创建csv文件
    writer = csv.writer(csvFile)                          #创建写的对象
    writer.writerow(["index","0Hz","100Hz","200Hz","300Hz","400Hz","500Hz","600Hz","700Hz","800Hz","900Hz","1000Hz"])     #写入列的名称               
    writer.writerows(excel)
    csvFile.close()
