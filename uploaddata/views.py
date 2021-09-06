from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.core.files.storage import FileSystemStorage
from config.models import mmDataset, mmProblem, mmRecipe, mmEquipspec
from django.db import transaction


from django.shortcuts import render, redirect, get_object_or_404

import os
import zipfile
import shutil

def createDirectory(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory)
            return True
        else:
            print('Already exists')
            return False
    except OSError: 
        print("Error: Failed to create the directory.")

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


class DataUploadView(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        context['username'] = request.user.username
        equip_name = request.GET.get('equip_name','')
        chamber_name = request.GET.get('chamber_name', '')
        recipe_name = request.GET.get('recipe_name', '')
        revision_no = request.GET.get('revision_no', '')
        rsEquip = mmEquipspec.objects.all().values_list('equip_name', flat=True).distinct()
        context['rsEquip'] = rsEquip
        if rsEquip and equip_name=='':
            equip_name = rsEquip[0]

        context['equip_name'] = equip_name

        rsChamber = mmEquipspec.objects.filter(equip_name=equip_name).values_list('chamber_name', flat=True).distinct()
        context['rsChamber'] = rsChamber
        if rsChamber and equip_name=='':
            chamber_name = rsChamber[0]
        context['chamber_name'] = chamber_name

        rsRecipe = mmRecipe.objects.filter(equip_name=equip_name).values_list('recipe_name', flat=True).distinct()
        context['rsRecipe'] = rsRecipe
        if rsRecipe and recipe_name == '':
            recipe_name = rsRecipe[0]
        context['recipe_name'] = recipe_name

        rsRevision = mmRecipe.objects.filter(equip_name=equip_name, recipe_name=recipe_name).values_list('revision_no', flat=True).distinct()
        context['rsRevision'] = rsRevision
        if rsRevision and revision_no=='':
            revision_no = rsRevision[0]
        context['revision_no'] = revision_no

        rsDataset = mmDataset.objects.filter(delete_flag='0').order_by('-id')
        context['rsDataset'] = rsDataset
        
        return render(request, 'dataupload.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        file = request.FILES.get('file', '')
        directory_name = request.POST['directory-name']
        type = request.POST['inlineRadioOptions']
        root_directory = directory_name.split('/')[0]

        #TST, TRN (db 저장코드)
        if type == 'train_data':
            purpose = 'TRN'
        elif type == 'test_data':
            purpose = 'TST'
        path = f'static/data/{type}/{directory_name}'
        
        if file == '':
            context['success'] = False
            context['message'] = '파일을 선택해주세요.'
            return JsonResponse(context, content_type='application/json')

        filename = file.name
        name_ext = os.path.splitext(filename)[1]

        if name_ext != '.zip':
            context['success'] = False
            context['message'] = 'zip 파일을 넣어주세요.'
            return JsonResponse(context, content_type='application/json')
        try:
            with transaction.atomic():
                if createDirectory(path):
                    fs = FileSystemStorage(location=path)
                    fs.save(f"{filename}", file)
                else:
                    context['success'] = False
                    context['message'] = '이미 존재하는 디렉토리 입니다.'
                    return JsonResponse(context, content_type='application/json')

                with zipfile.ZipFile(f'{path}/{filename}', 'r') as existing_zip:
                    data_name = existing_zip.namelist()[0][:-1]
                    save_path = f'{path}/{data_name}'
                    existing_zip.extractall(f'{path}')
                os.remove(f'{path}/{filename}')
                file_list = os.listdir(save_path)
                file_list = [name for name in file_list if name[0] != "." ] 

                # 파일갯수
                data_cnt = len(file_list)
                # 용량(바이트)
                data_size = get_dir_size(save_path)

                mmDataset.objects.create(
                    # id 값 바꿔야함!
                    # problem = mmProblem.objects.get(id=1),
                    data_static_path = '/' + save_path,
                    purpose = purpose,
                    data_name = data_name,
                    data_cnt = data_cnt,
                    data_size = data_size
                )
        except:
            shutil.rmtree(f'static/data/{type}/{root_directory}')
            context['success'] = False
            context['message'] = '업로드 실패!'
            return JsonResponse(context, content_type='application/json')


        context['success'] = True
        context['message'] = '업로드 성공!'
        return JsonResponse(context, content_type='application/json')