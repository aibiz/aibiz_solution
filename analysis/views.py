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

        query1 = request.GET.get('date_start', 'Null')
        query2 = request.GET.get('date_end','Null')
        if (query1=='Null') & (query2=='Null'):
            print("render!!!!")
            return render(request, "analysis.html", context)

        today = datetime.today().strftime("%Y-%m-%d")
        date_start = request.GET.get('date_start', today)
        date_end = request.GET.get('date_end', today)
        formatted_enddate = time.strptime(date_end,"%Y-%m-%d")
        formatted_startdate = time.strptime(date_start,"%Y-%m-%d")

        sensor_list = [2] #넘겨받아 split

        rootpath = os.getcwd()

        # 여러 챔버, 장비 선택시 for문 시작점
        # ex for path in selected_list:
        #       datapath = rootpath + path
        datapath = rootpath + "/static/data/train_data/11/recipe2" + '/' #server
        # datapath = rootpath + "/static/data/train_data/cc/recipe1" + '/'#local
        file_list = os.listdir(datapath)
        file_list_csv = [file for file in file_list if file.endswith(".csv")]
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
        #         if datetime.fromtimestamp(os.stat(datapath + filtered_filelist[i]).st_mtime) \
        #                 < datetime.fromtimestamp(os.stat(datapath + filtered_filelist[j]).st_mtime):
        #             print(filtered_filelist[i])
        #             (filtered_filelist[i], filtered_filelist[j]) = (filtered_filelist[j], filtered_filelist[i])

        d1_datasum = []
        csv_data = []
        for k in filtered_filelist:
            data = pandas.read_csv(datapath + k, header=None)
            for sensor_num in sensor_list:
                sensor_data = data.iloc[:, sensor_num]
                sensor_data = sensor_data.values.transpose().tolist()
                d1_data = np.reshape(sensor_data, -1)
                d1_datasum.extend(d1_data)
                csv_data.append([k, sensor_data])
        # end for selected_list

        #anomaly 데이터처리
        anomaly_path = rootpath + "/static/data/monitoring_anomalies" + '/'
        anomaly_file_list = os.listdir(anomaly_path)
        anomaly_csv_data = []

        #   파일을 수정시간순으로 정렬
        for i in range(0, len(anomaly_file_list)):
            for j in range(0, len(anomaly_file_list)):
                if datetime.fromtimestamp(os.stat(anomaly_path + anomaly_file_list[i]).st_mtime) \
                        < datetime.fromtimestamp(os.stat(anomaly_path + anomaly_file_list[j]).st_mtime):
                    (anomaly_file_list[i], anomaly_file_list[j]) = (anomaly_file_list[j], anomaly_file_list[i])
        #   파일 리스트 전체의 csv파일 데이터를 읽어들여와 List 형식으로 변환(전체파일)
        for k in anomaly_file_list:
            anomaly_data = pandas.read_csv(anomaly_path + k, header=None, )
            anomaly_data = anomaly_data.values.tolist()
            anomaly_csv_data.append(anomaly_data[0])
            anomaly_csv_data.append(anomaly_data[1])
            d1_datasum.extend(np.reshape(anomaly_data[0], -1))
            d1_datasum.extend(np.reshape(anomaly_data[1], -1))

        # mean, std
        mean_val = np.mean(d1_datasum)
        std_val = np.std(d1_datasum)
        print("mean::", mean_val, "std::", std_val)
        ori_data = []
        for j in range(0, len(csv_data)):
            ori_data.append(csv_data[j][1])
        # print("ori:::::::::::::", ori_data)

        # 정규화
        normalized_data = []
        normalized_anomaly_csvdata = []
        for l in range(0, len(csv_data)):
            normalized_data.append(list(map(lambda element: normalize(element, mean_val, std_val), ori_data[l])))
        for m in range(0, len(anomaly_csv_data)):
            normalized_anomaly_csvdata.append(list(map(lambda element: normalize(element, mean_val, std_val), anomaly_csv_data[m])))


        print("nomalized:::::::", normalized_data)

        context['raw_data'] = csv_data
        context['normalized_data']= normalized_data

        context['anomaly_filelist'] = anomaly_file_list
        context['anomaly_csvdata'] = anomaly_csv_data
        context['normalized_anomaly_csvdata'] = normalized_anomaly_csvdata

        # print("raw_data:::::::::", context['raw_data'])
        # print("normilized_data:::::::::", context['normalized_data'])
        # print("anomaly_filelist:::::::::::::", context['anomaly_filelist'])
        print("anomaly_csvdata::::::::::::", context['anomaly_csvdata'])
        print("normalized_csvdata::::::", context['normalized_anomaly_csvdata'])
        # print("response!!!!")
        return JsonResponse(context, content_type='application/json')

def normalize(element, mean, std):
    return (element-mean)/std