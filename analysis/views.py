from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
import os
import time
import pandas
from datetime import datetime
import numpy as np

class analysis_main(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        today = datetime.today().strftime("%Y-%m-%d")
        date_start = request.GET.get('date_start', today)
        date_end = request.GET.get('date_end', today)
        formatted_enddate = time.strptime(date_end,"%Y-%m-%d")
        formatted_startdate = time.strptime(date_start,"%Y-%m-%d")

        rootpath = os.getcwd()
        datapath = rootpath + "/static/data/train_data/aa/recipe1"
        file_list = os.listdir(datapath)
        file_list_csv= [file for file in file_list if file.endswith(".csv")]
        filtered_filelist = []

        # 기간내 파일 필터링
        for i in file_list_csv:
            date = i[:10]
            formatted_file_date = time.strptime(date, "%Y_%m_%d")
            if (formatted_startdate <= formatted_file_date and formatted_file_date <= formatted_enddate):
                filtered_filelist.append(i)
        # print(filtered_filelist)

        # for i in range(0, len(filtered_filelist)):
        #     for j in range(0, len(filtered_filelist)):
        #         if datetime.fromtimestamp(os.stat(datapath + '/'+ filtered_filelist[i]).st_mtime) \
        #                 < datetime.fromtimestamp(os.stat(datapath + '/' + filtered_filelist[j]).st_mtime):
        #             print(filtered_filelist[i])
        #             (filtered_filelist[i], filtered_filelist[j]) = (filtered_filelist[j], filtered_filelist[i])
        print(filtered_filelist)
        csv_data = []
        for k in filtered_filelist :
            data = pandas.read_csv(datapath +'/'+ k, header = None)
            rdata = data.iloc[:, 2]
            rdata = rdata.values.transpose().tolist()
            rdata = np.reshape(rdata, -1)
            break
            csv_data.append([k, data])
        print(data)
        mn = np.mean(rdata)
        std = np.std(rdata)
        print("mean:::",mn)
        print("std:::", std)
        for j in rdata:
            print((j - mn)/std)
        # print("std!!!!!!!!!!", np.std(csv_data))
        # print(csv_data)
        return render(request, "analysis.html", context)

