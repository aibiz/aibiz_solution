from django.shortcuts import render
from config.models import mmDataset
# from aiengine.learning_code import learn_anomaly

def training_main(request):
    context = {}

    trainDataList = mmDataset.objects.all().order_by('-id')[:50]
    testDataList = mmDataset.objects.all().order_by('-id')[:50]
    context['trainDataList'] = trainDataList
    context['testDataList'] = testDataList
    print(trainDataList)
    return render(request, 'training.html', context)


def start_training(request):
    print(request)



# Create your views here.
