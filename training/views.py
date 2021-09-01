from django.shortcuts import render
from config.models import mmDataset
import json
# from aiengine.learning_code import learn_anomaly

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

    trainDataId = rsData['trainDataId']
    testDataId = rsData['testDataId']
    sensorNo = rsData['sensorNo']
    thresholdStd = rsData['thresholdStd']
    print(trainDataId, testDataId, sensorNo, thresholdStd)

    if (trainDataId != 'Null' & testDataId != 'Null'):
       # learn_anomaly(sensorNo, thresholdStd, trainDataId)
        print("ttt")
    else:
        print("testdata or traindata가 입력되지 않았습니다.")





# Create your views here.
