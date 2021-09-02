from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.core.files.storage import FileSystemStorage
from config.models import mmDataset

from django.shortcuts import render, redirect, get_object_or_404

import os
import zipfile

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


class DataUploadView(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        context['username'] = request.user.username

        rsDataset = mmDataset.objects.filter(delete_flag='0')
        context['rsDataset'] = rsDataset
        
        return render(request, 'dataupload.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        file = request.FILES.get('file', '')
        directory_name = request.POST['directory-name']
        type = request.POST['inlineRadioOptions']
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

        if createDirectory(path):
            fs = FileSystemStorage(location=path)
            fs.save(f"{filename}", file)
        else:
            context['success'] = False
            context['message'] = '이미 존재하는 디렉토리 입니다.'
            return JsonResponse(context, content_type='application/json')

        with zipfile.ZipFile(f'{path}/{filename}', 'r') as existing_zip:
            save_path = f'{path}/{existing_zip.namelist()[0][:-1]}'
            print(save_path)
            existing_zip.extractall(f'{path}')
        os.remove(f'{path}/{filename}')
        file_list = os.listdir(save_path)
        file_list = [name for name in file_list if name[0] != "." ] 
        print(len(file_list)) #개수

        context['success'] = True
        context['message'] = '업로드 성공!'
        return JsonResponse(context, content_type='application/json')