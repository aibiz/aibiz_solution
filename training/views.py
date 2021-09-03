from django.shortcuts import render
from config.models import mmDataset
import json
import os
from .watchdog import *

import pandas
from aiengine.learning_code import learn_anomaly
from aiengine.test_code import test_anomaly



def training_main(request):
    context = {}

    trainDataList = mmDataset.objects.all().order_by('-id')[:50]
    testDataList = mmDataset.objects.all().order_by('-id')[:50]
    context['trainDataList'] = trainDataList
    context['testDataList'] = testDataList
    # print(trainDataList)
    return render(request, 'training.html', context)


def start_training(request):
    rsData = json.loads(request.body.decode("utf-8"))

    rootpath = os.getcwd()
    rootpath = rootpath.split('/')
    # rootpath = rootpath[:-1]
    rootpath = '/'.join(rootpath)

    trainDataId = rsData['trainDataId']
    trainStaticPath = mmDataset.objects.filter(id = trainDataId)[0].data_static_path
    trainStaticPath = rootpath + trainStaticPath

    testDataId = rsData['testDataId']
    testStaticPath = mmDataset.objects.filter(id = testDataId)[0].data_static_path
    testStaticPath = rootpath + testStaticPath

    sensorNo = int(rsData['sensorNo'])
    thresholdStd = int(rsData['thresholdStd'])
    print("path::", trainStaticPath, testStaticPath)
    print(trainDataId, testDataId, sensorNo, thresholdStd)
    if ((trainDataId != 'Null') & (testDataId != 'Null')):
        learn_anomaly(sensorNo, thresholdStd, trainStaticPath)
        test_anomaly(sensorNo, thresholdStd, testStaticPath)
    else:
        print("testdata, traindata모두 입력하세요.")

    result_train = Target()
    result_train.get_path(trainStaticPath)

def graphing_training(request):
    context = {}

    rsData = json.loads(request.body.decode("utf-8"))
    print("tstst", rsData)

    rootpath = os.getcwd()
    rootpath = rootpath.split('/')
    rootpath = rootpath[:-1]
    rootpath = '/'.join(rootpath)

    trainStaticPath = rsData['trainStaticPath']
    trainStaticPath = rootpath + trainStaticPath
    trainingStatusFile = trainStaticPath + "/after_learning/plots/training_status_loss.csv"
    trainingAnomalyFile = trainingStatusFile + "/after_learning/plots/train_anomaly_score.csv"

    testStaticPath = rsData['testStaticPath']
    testStaticPath = rootpath + testStaticPath
    testStatusFile = testStaticPath + "/after_test/anomolies/training_status_loss.csv"
    testAnomalyFile = testStaticPath + "/after_test/plots/training_status_loss.csv"


#     print("st_loss1:::", convert_data(trainingStatusFile, 0))
#     print("trainAnomaly:::", convert_data(trainingAnomalyFile, 0))
#     print("test_data:::", convert_data(testStatusFile, 0))
#     print("testAnomaly:::", convert_data(testAnomalyFile, 0))
#     # print("st_loss1:::", convert_data(trainingStatusFile)[0])
#     # print("st_loss2:::", convert_data(trainingStatusFile)[1])
#     # print("trainAnomaly:::", convert_data(trainingAnomalyFile)[0])
#     # print("test_data:::", convert_data(testStatusFile)[0])
#     # print("test_predict:::", convert_data(testStatusFile)[1])
#     # print("testAnomaly:::", convert_data(testAnomalyFile)[0])
#
#
#     # if(os.path.isfile(trainingAnomalyFile) & os.path.isfile(trainingAnomalyFile)
#     # & os.path.isfile(testStatusFile) & os.path.isfile(testAnomalyFile)):
#     #     context['status_loss']
#
# def convert_data(file,int mthd):
#     data = pandas.read_csv(file, header=None, encoding='cp949')
#     if(mthd == 1)
#             data.transpose()
#     data = data.values.tolist()
#     if(mthd == 1)
#         data = sum(data, [])
#     return data





