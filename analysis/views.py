from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
import os

class analysis_main(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        rootpath = os.getcwd()
        datapath = rootpath + "/static/data/train_data/aa/recipe1"
        file_list = os.listdir(datapath)
        for i in file_list:
            print(i)
            data_split = i.split('_')
        #     # if (data_split[0] > da

        return render(request, "analysis.html", context)

