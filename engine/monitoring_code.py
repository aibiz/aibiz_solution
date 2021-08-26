import numpy as np
from matplotlib import pyplot as plt
import  pickle
from csv import reader
from keras.models import load_model
import os
import pandas as pd
from gen_tensor import gen_tensor_for_test

def test_anomaly(sensor_num, input_data_path, input_file_path, output_path):
    '''
    input
    sensor_num : sensor 번호
    input_data_path : test_data의 file 경로
    input_file_path : input file 경로
     sensor#.5h : 학습된 모델
     threshhod.txt : 학습했을때의 Threshhold

    output
    anomolies : 불량으로 판정된 Wafer list의 csv file
    '''
    filename = os.path.basename(input_data_path)
    input_path = os.path.dirname(input_data_path)
    f = open(f"{input_file_path}\\after_learning\\test_input\\data_length.txt", 'r')
    data_length = int(f.readline())
    f.close()

    csv_data = pd.read_csv(input_data_path, header=None).to_numpy()
    r, c = np.shape(csv_data)
    monitoring_data = np.zeros((1, data_length, c))

    for i in range(0, r):
        for j in range(0, c):
            monitoring_data[0, i, j] = csv_data[i, j]


    f = open(f"{input_file_path}\\after_learning\\test_input\\threshold.txt", 'r')
    threshold = float(f.readline())
    f.close()

    '''
    iput file 입력 및 확인
    '''
    t=[]
    monitoring_data = monitoring_data[:,:,sensor_num]
    r, c = np.shape(monitoring_data)
    monitoring_data = np.reshape(monitoring_data, (r,c,1))


    with open(f'{input_file_path}\\wafer_list.pickle', 'rb') as f:
        w_info = pickle.load(f)
        w_info = list(w_info)

    with open(f'{input_file_path}\\sensor_info.txt', 'r') as csv_file:
        s_info = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        s_info = list(s_info)

    model = load_model(f"{input_file_path}\\after_learning\\test_input\\sensor_{sensor_num}.h5")
    model.summary()


    '''
    Normalization
    '''
    testing_mean = monitoring_data.mean()
    testing_std = monitoring_data.std()
    df_testing_value = (monitoring_data - testing_mean) / testing_std

    xtest = df_testing_value

    x_test_pred = model.predict(xtest)
    x_test_unno = (xtest * testing_std) + testing_mean
    x_test_pred_unno = (x_test_pred * testing_std) + testing_mean

    test_mae_loss = np.mean(np.abs((x_test_pred_unno) - (x_test_unno)), axis=1)

    hist, bins = np.histogram(test_mae_loss, 60)


    # plt.hist(test_mae_loss, bins=50)


    print("Threshhold 값: ", threshold)

    anomalies = test_mae_loss > threshold
    print("Anomaly 수: ", np.sum(anomalies))

    if anomalies == 1:
        temp1 = x_test_unno[0]
        temp2 = x_test_pred_unno[0]
        t_csv = np.stack((temp1[:, 0], temp2[:, 0]))
        np.savetxt(f"{output_path}\\{filename}", t_csv, delimiter=",", fmt="%s")


'''
input_path = 'monitoring\\2020_07_10_0164660_4.csv'
input_file_path = "train_data\\recipe1"
sensor_num = 2

test_anomaly(sensor_num, input_path, input_file_path)

'''