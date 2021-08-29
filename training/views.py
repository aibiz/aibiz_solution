from django.shortcuts import render
from config.models import mmDataset

def training_main(request):
    context = {}

    datalist = mmDataset.objects.all().order_by('-id')[:30]
    context['dataList'] = datalist
    print(datalist)
    return render(request, 'training.html', context)


# def traindata_select():



# Create your views here.
