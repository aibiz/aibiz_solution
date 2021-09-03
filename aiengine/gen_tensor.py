import os
import numpy as np
import pandas as pd
from keras.preprocessing import sequence
import pickle

def gen_tensor(input_path):
    '''
    input path의 .CSV data를 읽고 하나의 tensor로 변경 시간축은 normalize
    data_path: Input Folder가 모두 있는 folder
    output : output.npy (.CSV file로 부터 만들어진 Tensor)
    '''
    file_name = os.path.basename(input_path)
    file_ext = r".csv"
    print(f"{file_name}의 tensor 생성 중")
    raw_list= [file for file in os.listdir(input_path) if file.endswith(file_ext)]
    if len(raw_list) > 5:
        data_temp = []
        length = len(raw_list)
        total = 0
        for file in raw_list:
            csv_data = pd.read_csv(input_path + '/' + file, header=None)
            data_temp2 = []
            for j in csv_data.columns:
                data_temp2.append(csv_data[j].tolist())
            n_sen, c = (np.shape(data_temp2))
            total += c
        ave = int(total//length)

        w_list = []
        for file in raw_list:
            csv_data = pd.read_csv(input_path + '/' + file, header=None)
            data_temp2 = []

            for j in csv_data.columns:
                data_temp2.append(csv_data[j].tolist())
            r, c = (np.shape(data_temp2))

            if (c <= ave+20):
                w_list.append(file)
                data_temp.extend(data_temp2)
        X_prime = sequence.pad_sequences(data_temp, padding='post', value=99999, dtype=float)
        r, c = np.shape(X_prime)
        X_prime = X_prime.reshape((-1, n_sen, c), order='C')
        X_prime = X_prime.transpose(0, 2, 1)

        d, r, c = np.shape(X_prime)
        '''Time initilization'''
        for k in range(0, d):
            for j in range(0, r):
                if X_prime[k, r - j - 1, 0] != 99999:
                    X_prime[k, r - j - 1, 0] = abs(X_prime[k, r - j - 1, 0] - X_prime[k, 0, 0])

        np.save(f"{input_path}"+ "/" +  "output.npy", X_prime)
        with open(f"{input_path}"+"/"+  "wafer_list.pickle", 'wb') as f:
            pickle.dump(w_list, f)

        print("x_prime:::", X_prime)
        print("tensor 생성 완료!")

def gen_tensor_for_test(input_data_path, input_file_path):
    '''
    input path의 .CSV data를 읽고 하나의 tensor로 변경 시간축은 normalize
    data_path: Input Folder가 모두 있는 folder
    output : output.npy (.CSV file로 부터 만들어진 Tensor)
    '''
    f = open(f"{input_file_path}/after_learning/test_input/data_length.txt", 'r')
    data_length = float(f.readline())
    f.close()

    file_name = os.path.basename(input_data_path)
    file_ext = r".csv"
    print(f"{file_name}의 tensor 생성 중")
    raw_list= [file for file in os.listdir(input_data_path) if file.endswith(file_ext)]
    if len(raw_list) > 5:
        data_temp = []
        length = len(raw_list)
        total = 0
        for file in raw_list:
            csv_data = pd.read_csv(input_data_path + '/' + file, header=None)
            data_temp2 = []
            for j in csv_data.columns:
                data_temp2.append(csv_data[j].tolist())
            n_sen, c = (np.shape(data_temp2))
            total += c
        ave = int(total//length)

        w_list = []
        for file in raw_list:
            csv_data = pd.read_csv(input_data_path + '/' + file, header=None)
            data_temp2 = []

            for j in csv_data.columns:
                data_temp2.append(csv_data[j].tolist())
            r, c = (np.shape(data_temp2))

            if (c <= data_length):
                w_list.append(file)
                data_temp.extend(data_temp2)
        X_prime = sequence.pad_sequences(data_temp, padding='post', value=99999, dtype=float)
        r, c = np.shape(X_prime)
        X_prime = X_prime.reshape((-1, n_sen, c), order='C')
        X_prime = X_prime.transpose(0, 2, 1)

        d, r, c = np.shape(X_prime)
        '''Time initilization'''
        for k in range(0, d):
            for j in range(0, r):
                if X_prime[k, r - j - 1, 0] != 99999:
                    X_prime[k, r - j - 1, 0] = abs(X_prime[k, r - j - 1, 0] - X_prime[k, 0, 0])

        np.save(f"{input_data_path}"+ "/" +  "output.npy", X_prime)
        with open(f"{input_data_path}"+"/"+  "wafer_list.pickle", 'wb') as f:
            pickle.dump(w_list, f)


        print("tensor 생성 완료!")


'''
"******Excution method******"
input_path = 'monitoring/2020_07_10_0164660_1.csv'
input_file_path = "train_data/recipe1"
sensor_num = 2

gen_tensor_for_test(input_path, input_file_path)
'''