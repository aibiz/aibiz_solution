from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from config.models import mmModel, mmProblem, mmDataset

class masterdatamain(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, 'masterdata/masterdatamain.html', context)

class masterdataequipfind(View) :
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        data = mmModel.objects.all()
        print(data.values())
        context['data'] = list(data.values())

        return JsonResponse(context, content_type='application/json')

class masterdataproblemfind(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        data = mmProblem.objects.all()
        print(data.values())
        context['data'] = list(data.values())

        return JsonResponse(context, content_type='application/json')

class masterdatadatasetfind(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        data = mmDataset.objects.all()
        print(data.values())
        context['data'] = list(data.values())

        return JsonResponse(context, content_type='application/json')

class equipmentdatamodify(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.GET['id']
        data = mmModel.objects.get(id=id)
        print(data)
        context = {
            'data' : data
        }

        return render(request, 'masterdata/equipdatamodify.html', context)


