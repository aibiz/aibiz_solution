import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt
import gzip, pickle
from keras.models import load_model
from csv import reader
import os
from .gen_tensor import gen_tensor

def learn_anomaly(sensor_num, tresh_num, input_path):

    '''
    input
    sensor_num : .csv file에 있는 sensor 번호
    tresh_num : threshold를 찹기 위한 값
    input_path : data가 있는 path (아래 file들을 받아드림)
       output.npy : .csv file로 부터 만들어진 tensor (.npy file) gen_tensor의 output
       sensor info.txt : input data의 sensor info
       wafer_list.pickle : 학습한 데이터의 Wafer 정보

    output
    .h5 file : 학습된 Model
    .anomalies : 학습 중 불량으로 판단된 이상치
    threshhold.txt : 학습 후 찾아낸 defalt threshhold값
    '''
    gen_tensor(input_path)
    print("learn::::", sensor_num, tresh_num)
    if not os.path.isdir(f"{input_path}/after_learning"):
        os.mkdir(f"{input_path}/after_learning")
        os.mkdir(f"{input_path}/after_learning/test_input")
        os.mkdir(f"{input_path}/after_learning/anomalies")
        os.mkdir(f"{input_path}/after_learning/plots")

    '''
    iput file 입력 및 확인
    '''
    train_data = np.load(f"{input_path}/output.npy")
    train_data = train_data[:,:,sensor_num]
    r, c = np.shape(train_data)
    train_data = np.reshape(train_data, (r,c,1))

    f = open(f"{input_path}/after_learning/test_input/data_length.txt", 'w')
    f.write(str(c))
    f.close()

    with open(f'{input_path}'+'/'+ 'wafer_list.pickle', 'rb') as f:
        w_info = pickle.load(f)
        w_info = list(w_info)

    with open(f'{input_path}'+'/'+'sensor_info.txt', 'r') as csv_file:
        s_info = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        s_info = list(s_info)

    '''
    Plot Data
    '''
    for i in range(0, r):
        n_pad = train_data[i, :,0].tolist().count(99999)
        m = c - n_pad
        plt.plot(train_data[i,0:m,0], label='Sensor data')
        plt.title(f"{s_info[0][sensor_num]}")
        plt.xlabel("Time")
        plt.ylabel("Sensor Value")
    plt.show()

    '''
    padding value to zero
    '''
    train_data = np.where(train_data == 99999, 0, train_data)

    '''
    Normalization
    '''
    training_mean = train_data.mean()
    training_std = train_data.std()
    df_training_value = (train_data - training_mean) / training_std

    xtrain = df_training_value

    print("Number of training samples:", len(xtrain))
    #
    model = keras.Sequential(
        [

            layers.Input(shape=(xtrain.shape[1], xtrain.shape[2])),
            layers.Conv1D(
                filters=64, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1D(
                filters=32, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1D(
                filters=16, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1D(
                filters=8, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1D(
                filters=4, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Conv1DTranspose(
                filters=4, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1DTranspose(
                filters=8, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1DTranspose(
                filters=16, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1DTranspose(
                filters=32, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Dropout(rate=0.2),
            layers.Conv1DTranspose(
                filters=64, kernel_size=7, padding="same", strides=1, activation="relu"
            ),
            layers.Conv1DTranspose(filters=1, kernel_size=7, padding="same"),
        ]
    )
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss="mse")
    model.summary()

    #
    history = model.fit(
        xtrain,
        xtrain,
        epochs=50,
        batch_size=128,
        validation_split=0.1,
        callbacks=[
            keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, mode="min")
        ],
    )
    model.save(f'{input_path}/after_learning/test_input/sensor_{sensor_num}.h5')

    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.legend()
    plt.show()
    temp1 = history.history["loss"]
    temp2 = history.history["val_loss"]
    t_csv = np.stack((temp1[:], temp2[:]))
    np.savetxt(f"{input_path}/after_learning/plots/Training_status_loss.csv", t_csv, delimiter=",", fmt="%s")

    x_train_pred = model.predict(xtrain)
    x_train_unno = (xtrain * training_std) + training_mean
    x_train_pred_unno = (x_train_pred * training_std) + training_mean

    train_mae_loss = np.mean(np.abs((x_train_pred_unno) - (x_train_unno)), axis=1)

    thresh = []
    hist, bins = np.histogram(train_mae_loss, 60)
    hist = np.append(hist, np.array([0]))
    for i in range(0, len(hist)):
        if hist[i] < tresh_num:
            thresh.append(bins[i])
        if max(hist) == hist[i]:
            peak_loc = i

    peak = bins[peak_loc]

    zero = 0
    thresh2=[]
    for i in range(0, len(thresh)):
        if thresh[i] > peak:
            thresh2.append(thresh[i])
    threshold = min(thresh2)


    f = open(f"{input_path}/after_learning/test_input/threshold.txt", 'w')
    f.write(str(threshold))
    f.close()




    # plt.hist(train_mae_loss, bins=50)
    plt.hist(train_mae_loss, bins=60)
    plt.title("Trained Data - Predicted Data")
    plt.xlabel("Train MAE loss")
    plt.ylabel("No of samples")
    plt.show()
    np.savetxt(f"{input_path}/after_learning/plots/train_anomaly_score.csv", train_mae_loss, delimiter=",", fmt="%s")

    print("Threshhold 값: ", threshold)

    anomalies = train_mae_loss > threshold
    print("Anomaly 수: ", np.sum(anomalies))

    k=1
    for i in range(0, len(x_train_pred_unno)):
        if train_mae_loss[i] > threshold:
            plt.subplot(5, 5, k)
            plt.plot(x_train_unno[i], label='Training Data')
            plt.plot(x_train_pred_unno[i], label='Predicted')
            plt.title(f"{w_info[i].replace('.csv','')}")
            plt.xlabel("Time")
            plt.ylabel("Sensor Value")
            plt.legend()
            k=k+1
            temp1= x_train_unno[i]
            temp2= x_train_pred_unno[i]
            t_csv = np.stack((temp1[:,0], temp2[:,0]))
            np.savetxt(f"{input_path}/after_learning/anomalies/{w_info[i]}", t_csv, delimiter=",", fmt="%s")
            if k > 25:
                plt.subplots_adjust(wspace=0.3, hspace=0.8)
                plt.show()
                k=1
    plt.subplots_adjust(wspace=0.3, hspace=0.8)
    plt.show()

"******Excution method******"

sensor_num = 2
tresh_num = 10

# abspath = os.getcwd()
# print(abspath)
# input_path = abspath + "/aiengine/train_data/recipe1"
#
# learn_anomaly(sensor_num, tresh_num, input_path)