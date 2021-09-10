from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from config.models import mmModel, mmDataset, mmRecipe
from aiengine.monitoring_excute import Target
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render, redirect, get_object_or_404

import os
import csv
import datetime
import pandas
import json

monitoring = None

class monitoringmain(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        #초기화시 장비에 대한 기본 정보 전체 조회
        equip_sql = '''
            SELECT id, equip_name FROM mm_dataset WHERE purpose='TRN' GROUP BY equip_name 
        '''

        context = {
            'equip_select': mmModel.objects.raw(equip_sql)
        }

        return render(request, 'monitoring/monitoringmain.html', context)

class find_chamber(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        rsData = json.loads(request.body.decode("utf-8"))
        equip_name = rsData['equip_name']
        data = mmDataset.objects.filter(equip_name=equip_name, purpose="TRN").values_list('chamber_name', flat=True).distinct()

        context = {
            'chamber_list': list(data)
        }

        return JsonResponse(context, content_type='application/json')

class find_recipe(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        rsData = json.loads(request.body.decode("utf-8"))
        chamber_name = rsData['chamber_name']
        data = mmDataset.objects.filter(chamber_name=chamber_name, purpose="TRN").values_list('recipe_name', flat=True).distinct()

        context = {
            'recipe_list': list(data)
        }

        return JsonResponse(context, content_type='application/json')

class find_revision(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        rsData = json.loads(request.body.decode("utf-8"))
        recipe_name = rsData['recipe_name']
        data = mmDataset.objects.filter(recipe_name=recipe_name, purpose="TRN").values_list('revision_no', flat=True).distinct()

        context = {
            'revision_list': list(data)
        }

        return JsonResponse(context, content_type='application/json')

class find_sensor(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        rsData = json.loads(request.body.decode("utf-8"))
        equip_name = rsData['equip_name']
        chamber_name = rsData['chamber_name']
        recipe_name = rsData['recipe_name']
        revision_no = rsData['revision_no']
        data = mmRecipe.objects.filter(equip_name=equip_name, chamber_name=chamber_name, recipe_name=recipe_name, revision_no=revision_no)

        context = {
            'sensor_list': list(data.values())
        }

        return JsonResponse(context, content_type='application/json')

class run_monitoring(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        global monitoring   #global 변수로 선언하여 센서 재선택시 기존 thread가 중단되도록 설정
        context = {}

        #기존 thread가 존재하는 경우 기존 thread 중단
        if monitoring != None :
            monitoring.run_stop()

        rootpath = os.getcwd()
        rootpath = rootpath.split('/')
        # rootpath = rootpath[:-1]
        rootpath = '/'.join(rootpath)

        #모니터링 후 에러 파일 저장 디렉토리
        anomalies_path = rootpath + "/static/data/monitoring_anomalies/"

        #모니터링을 진행할 파일 업로드 경로
        monitoring_path = rootpath + '/static/data/monitoring'

        rsData = json.loads(request.body.decode("utf-8"))
        equip_name = rsData['equip_name']
        chamber_name = rsData['chamber_name']
        recipe_name = rsData['recipe_name']
        sensor_cd = rsData['sensor_cd']

        #학습 파일 경로 파악
        data = mmDataset.objects.filter(equip_name=equip_name, chamber_name=chamber_name, recipe_name=recipe_name, purpose='TRN').values_list('data_static_path', flat=True)
        path = rootpath + data[len(data) - 1]

        #test용으로 센서 번호만 이렇게..
        #sensor_cd = 2

        #모니터링 작업을 위한 watchdog thread 생성
        #모니터링 경로가 존재하지 않는 경우에는 watchdog thread 실행후 센서 변경시 런타임 에러가 발생하므로
        #모니터링 파일 경로가 존재하는 경우에만 기능 동작하도록 처리
        if os.path.isdir(monitoring_path):
            monitoring = Target()
            monitoring.get_path(monitoring_path, sensor_cd, path, anomalies_path)
            monitoring.daemon = True
            monitoring.run()
        else:
            context['success'] = False
            context['message'] = '경로가 존재하지 않아 실행할 수 없습니다!'
            return JsonResponse(context, content_type='application/json')

        return JsonResponse(context, content_type='application/json')


class monitoring_upload(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        file = request.FILES.get('file', '')
        directory_name = request.POST['dir']

        path = f'static/data/{directory_name}'

        if file == '':
            context['success'] = False
            context['message'] = '파일을 선택해주세요.'
            return JsonResponse(context, content_type='application/json')

        filename = file.name
        name_ext = os.path.splitext(filename)[1]
        
        #csv 파일만 저장되도록 지정
        if name_ext != '.csv':
            context['success'] = False
            context['message'] = 'csv 파일을 넣어주세요.'
            return JsonResponse(context, content_type='application/json')

        try:
            fs = FileSystemStorage(location=path)
            fs.save(f"{filename}", file)
            print(fs)
        except:
            context['success'] = False
            context['message'] = '업로드에 실패하였습니다.'
            return JsonResponse(context, content_type='application/json')

        context['success'] = True
        context['message'] = '업로드에 성공하였습니다.'
        return JsonResponse(context, content_type='application/json')

class execute_monitoring(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        rootpath = os.getcwd()
        rootpath = rootpath.split('/')
        # rootpath = rootpath[:-1]
        rootpath = '/'.join(rootpath)

        dir = rootpath + "/static/data/monitoring_anomalies/"
        file_list = os.listdir(dir)
        csv_list = []

        #파일을 수정시간순으로 정렬
        file_list.sort(key=lambda s: os.stat(os.path.join(dir, s)).st_mtime)

        '''for i in range(0, len(file_list)) :
            for j in range(0, len(file_list)) :
                if datetime.datetime.fromtimestamp(os.stat(dir + file_list[i]).st_mtime) < datetime.datetime.fromtimestamp(os.stat(dir + file_list[j]).st_mtime) :
                    (file_list[i], file_list[j]) = (file_list[j], file_list[i])'''

        #파일 리스트 전체의 csv파일 데이터를 읽어들여와 List 형식으로 변환(전체파일)
        for k in file_list :
            data = pandas.read_csv(dir + k, header = None)
            data = data.values.tolist()
            csv_list.append([k, data])

        context = {
            "anomalies_list": file_list,
            "csv_list" : csv_list
        }

        return JsonResponse(context, content_type='application/json')

class stop_thread(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        #global 변수를 이용하여 페이지를 종료하거나 이동하는 경우 기존에 동작중이던 모니터링 thread를 중단시킨다.
        global monitoring
        context = {}

        if monitoring != None :
            monitoring.run_stop()

        return JsonResponse(context, content_type='application/json')
