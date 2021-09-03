import numpy as np
from matplotlib import pyplot as plt
import  pickle
from csv import reader
from keras.models import load_model
import os
from .gen_tensor import gen_tensor_for_test

def test_anomaly(sensor_num, input_data_path, input_file_path):
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
    gen_tensor_for_test(input_data_path, input_file_path)

    if not os.path.isdir(f"{input_data_path}/after_test"):
        os.mkdir(f"{input_data_path}/after_test")
        os.mkdir(f"{input_data_path}/after_test/anomalies")
        os.mkdir(f"{input_data_path}/after_test/plots")

    f = open(f"{input_file_path}/after_learning/test_input/threshold.txt", 'r')
    threshold = float(f.readline())
    f.close()
    '''
    iput file 입력 및 확인
    '''
    t=[]
    test_data = np.load(f"{input_data_path}/output.npy")
    test_data = test_data[:,:,sensor_num]
    r, c = np.shape(test_data)
    test_data = np.reshape(test_data, (r,c,1))


    with open(f'{input_data_path}/wafer_list.pickle', 'rb') as f:
        w_info = pickle.load(f)
        w_info = list(w_info)

    with open(f'{input_data_path}/sensor_info.txt', 'r') as csv_file:
        s_info = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        s_info = list(s_info)

    model = load_model(f"{input_file_path}/after_learning/test_input/sensor_{sensor_num}.h5")
    model.summary()

    '''
    padding to zero
    '''
    test_data = np.where(test_data == 99999, 0, test_data)

    '''
    Normalization
    '''
    testing_mean = test_data.mean()
    testing_std = test_data.std()
    df_testing_value = (test_data - testing_mean) / testing_std

    xtest = df_testing_value

    x_test_pred = model.predict(xtest)
    x_test_unno = (xtest * testing_std) + testing_mean
    x_test_pred_unno = (x_test_pred * testing_std) + testing_mean

    test_mae_loss = np.mean(np.abs((x_test_pred_unno) - (x_test_unno)), axis=1)

    hist, bins = np.histogram(test_mae_loss, 60)


    # plt.hist(test_mae_loss, bins=50)
    plt.hist(test_mae_loss, bins=60)
    plt.title("tested Data - Predicted Data")
    plt.xlabel("test MAE loss")
    plt.ylabel("No of samples")
    plt.show()
    np.savetxt(f"{input_path}/after_test/plots/test_anomaly_score.csv", test_mae_loss, delimiter=",", fmt="%s")

    print("Threshhold 값: ", threshold)

    anomalies = test_mae_loss > threshold
    print("Anomaly 수: ", np.sum(anomalies))

    k=1
    for i in range(0, len(x_test_pred_unno)):
        if test_mae_loss[i] > threshold:
            plt.subplot(5, 5, k)
            plt.plot(x_test_unno[i], label='testing Data')
            plt.plot(x_test_pred_unno[i], label='Predicted')
            plt.title(f"{w_info[i].replace('.csv','')}")
            plt.xlabel("Time")
            plt.ylabel("Sensor Value")
            plt.legend()
            k=k+1
            temp1= x_test_unno[i]
            temp2= x_test_pred_unno[i]
            t_csv = np.stack((temp1[:,0], temp2[:,0]))
            np.savetxt(f"{input_data_path}/after_test/anomalies/{w_info[i]}", t_csv, delimiter=",", fmt="%s")
            if k > 25:
                plt.subplots_adjust(wspace=0.3, hspace=0.8)
                plt.show()
                k=1
    plt.subplots_adjust(wspace=0.3, hspace=0.8)
    plt.show()
input_path = 'test_data/recipe1'
input_file_path = "train_data/recipe1"
sensor_num = 2


# test_anomaly(sensor_num, input_path, input_file_path)

