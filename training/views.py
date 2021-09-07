from django.views.generic import View
from django.shortcuts import render
from config.models import mmDataset, mmModel
import json
import os
from django.http import HttpRequest, JsonResponse
import datetime
import pandas
from aiengine.learning_code import learn_anomaly
from aiengine.test_code import test_anomaly


def training_main(request):
    context = {}

    trainDataList = mmDataset.objects.filter(purpose="TRN").order_by('-id')[:50]
    testDataList = mmDataset.objects.filter(purpose="TST").order_by('-id')[:50]
    context['trainDataList'] = trainDataList
    context['testDataList'] = testDataList
    return render(request, 'training.html', context)


def start_training(request):
    context = {}
    rsData = json.loads(request.body.decode("utf-8"))
    print("!!!!!!!!!!!!!Start Training!!!!!!!!!!!!!")

    rootpath = os.getcwd()
    rootpath = rootpath.split('/')
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
        test_anomaly(sensorNo, testStaticPath, trainStaticPath)
        print("!!!!!!!!!!!!!End Training!!!!!!!!!!!!!")
    else:
        print("testdata, traindata모두 입력하세요.")
    return JsonResponse(context, content_type='application/json')


def graphing_training(request):
    context = {}

    rsData = json.loads(request.body.decode("utf-8"))

    rootpath = os.getcwd()

    trainStaticPath = rsData['trainStaticPath']
    trainStaticPath = rootpath + trainStaticPath
    trainingStatusFile = trainStaticPath + "/after_learning/plots/Training_status_loss.csv"
    trainingAnomalyFile = trainStaticPath + "/after_learning/plots/train_anomaly_score.csv"
    thresholdFile = trainStaticPath + "/after_learning/test_input/threshold.txt"

    testStaticPath = rsData['testStaticPath']
    testStaticPath = rootpath + testStaticPath
    testAnomalyFile = testStaticPath + "/after_test/plots/test_anomaly_score.csv"
    testAnomalyList = testStaticPath + '/after_test/anomalies/'


    if(os.path.isfile(trainingAnomalyFile) & os.path.isfile(trainingAnomalyFile) & os.path.isfile(testAnomalyFile)):
        # dir = testStaticPath + '/after_test/anomalies/'
        #3번그래프 데이터처리
        file_list = os.listdir(testAnomalyList)
        csv_list = []
        #   파일을 수정시간순으로 정렬
        for i in range(0, len(file_list)) :
            for j in range(0, len(file_list)) :
                if datetime.datetime.fromtimestamp(os.stat(testAnomalyList + file_list[i]).st_mtime) \
                        < datetime.datetime.fromtimestamp(os.stat(testAnomalyList + file_list[j]).st_mtime) :
                    (file_list[i], file_list[j]) = (file_list[j], file_list[i])
        #   파일 리스트 전체의 csv파일 데이터를 읽어들여와 List 형식으로 변환(전체파일)
        for k in file_list :
            data = pandas.read_csv(testAnomalyList + k, header = None)
            data = data.values.tolist()
            csv_list.append([k, data])

        #threshold
        thresholdpd = pandas.read_csv(thresholdFile, header=None)
        threshold = pandas.DataFrame(thresholdpd).loc[0, 0]
        print("threshold:::", threshold)
        context = {
            'anomalies_list': file_list,
            'csv_list' : csv_list,
            'current_threshold' : threshold,
            'status_loss' : convert_data(trainingStatusFile, 0)[0],
            'status_val_loss' : convert_data(trainingStatusFile, 0)[1],
            'train_anomaly_score' : convert_data(trainingAnomalyFile, 1),
            'test_anomaly_score' : convert_data(testAnomalyFile, 1)
        }

        # mmModel.objects.create(
        #
        # )
        # context['status_loss'] = convert_data(trainingStatusFile, 0)[0]
        # context['status_val_loss'] = convert_data(trainingStatusFile, 0)[1]
        # context['train_anomaly_score'] = convert_data(trainingAnomalyFile, 1)
        # context['test_anomaly_score'] = convert_data(testAnomalyFile, 1)

        # print("status_loss'", context['status_loss'])
        # print("test_anomaly_score", context['test_anomaly_score'])
        context['state'] = "True"
        return JsonResponse(context, content_type='application/json')
    else :
        context['state'] = "False"
        return JsonResponse(context, content_type='application/json')


def convert_data(file, mthd):
    data = pandas.read_csv(file, header=None, encoding='cp949')
    # 1차원 수직행렬의 경우만 mthd = 1
    if(mthd == 1):
        data.transpose()
    data = data.values.tolist()
    if(mthd == 1):
        data = sum(data, [])
    return data








