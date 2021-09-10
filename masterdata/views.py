from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from config.models import mmRecipe, mmProblem, mmDataset
from django.db import transaction

class masterdatamain(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, 'masterdata/masterdatamain.html', context)

class masterdatarecipefind(View) :
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        data = mmRecipe.objects.all()
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

        context = {
            'data' : data
        }

        return render(request, 'masterdata/equipdatamodify.html', context)

class update_equipment(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        print(request.POST)
        id = request.POST['id']
        id = request.POST['id']

        data = mmDataset.objects.all()
        print(data.values())
        context['data'] = list(data.values())

        return JsonResponse(context, content_type='application/json')

class problemdatamodify(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.GET['id']
        data = mmProblem.objects.get(id=id)

        context = {
            'data' : data
        }

        return render(request, 'masterdata/problemmodify.html', context)

class update_problem(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.POST['id']
        problem_name = request.POST['problem_name']
        problem_note = request.POST['problem_note']

        try:
            with transaction.atomic():
                data = mmProblem.objects.get(id=id)
                data.problem_name = problem_name
                data.problem_note = problem_note
                data.save()
        except:
            context['success'] = False
            context['message'] = "수정에 실패하였습니다."
            return JsonResponse(context, content_type='application/json')

        context['success'] = True
        context['message'] = "수정되었습니다."

        return JsonResponse(context, content_type='application/json')

class delete_problem(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.POST['id']

        try:
            with transaction.atomic():
                data = mmProblem.objects.get(id=id)
                data.delete()
        except:
            context['success'] = False
            context['message'] = "삭제에 실패하였습니다."
            return JsonResponse(context, content_type='application/json')

        context['success'] = True
        context['message'] = "삭제되었습니다."

        return JsonResponse(context, content_type='application/json')

class datasetdatamodify(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.GET['id']
        data = mmDataset.objects.get(id=id)

        context = {
            'data' : data
        }

        return render(request, 'masterdata/datasetmodify.html', context)

class update_dataset(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.POST['id']

        try:
            with transaction.atomic():
                data = mmDataset.objects.get(id=id)
                data.equip_name = request.POST['equip_name']
                data.chamber_name = request.POST['chamber_name']
                data.recipe_name = request.POST['recipe_name']
                data.data_static_path = request.POST['data_static_path']
                data.purpose = request.POST['purpose']
                data.data_name = request.POST['data_name']
                data.save()
        except:
            context['success'] = False
            context['message'] = "수정에 실패하였습니다."
            return JsonResponse(context, content_type='application/json')

        context['success'] = True
        context['message'] = "수정되었습니다."

        return JsonResponse(context, content_type='application/json')

class delete_dataset(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.POST['id']

        try:
            with transaction.atomic():
                data = mmDataset.objects.get(id=id)
                data.delete()
        except:
            context['success'] = False
            context['message'] = "삭제에 실패하였습니다."
            return JsonResponse(context, content_type='application/json')

        context['success'] = True
        context['message'] = "삭제되었습니다."

        return JsonResponse(context, content_type='application/json')


