from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.core.files.storage import FileSystemStorage
from config.models import mmDataset

from django.shortcuts import render, redirect, get_object_or_404

import os

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
        print(file)
        if file == '':
            context['success'] = False
            context['message'] = '파일을 선택해주세요.'

        filename = file.name
        name_ext = os.path.splitext(filename)[1]

        if os.path.isfile('static/' + filename):
            os.remove('static/' + filename)

        fs = FileSystemStorage(location='static')

        name = fs.save(f"{filename}", file)

        context['success'] = True
        context['message'] = '업로드 성공!.'
        return JsonResponse(context, content_type='application/json')