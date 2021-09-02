from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from config.models import mmModel

from django.shortcuts import render, redirect, get_object_or_404

import os
import csv

class monitoringmain(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        sql = '''
            SELECT MD.id, MD.problem_id, MD.equipment_id, MD.chamber_id, MD.recipe_no, MD.sensor_no, MD.dataset_id, DS.data_static_path
            FROM mm_model MD
            LEFT OUTER JOIN mm_dataset DS ON MD.dataset_id = DS.id
            ORDER BY MD.id
        '''

        #Tree 구현을 위해 각 장비, Chamber, Recipe 별로 카운트를 구해서 처리한다.
        tree_sql = '''
            SELECT 
                id,
                equipment_id, 
                chamber_id, 
                recipe_no, 
                sensor_no,
                eqip_cnt,
                cham_cnt,
                rec_cnt
            FROM(
                SELECT 
                    id,
                    equipment_id, 
                    chamber_id, 
                    recipe_no, 
                    sensor_no,
                    (CASE @gru_eqip WHEN equipment_id THEN @num_eqip:=@num_eqip+1 ELSE @num_eqip:=1 END) AS eqip_cnt,
                    (@gru_eqip:=equipment_id) AS tmp_eqip,
                    (CASE @gru_cham WHEN chamber_id THEN @num_cham:=@num_cham+1 ELSE @num_cham:=1 END) AS cham_cnt,
                    (@gru_cham:=chamber_id) AS tmp_cham,
                    (CASE @gru_rec WHEN recipe_no THEN @num_rec:=@num_rec+1 ELSE @num_rec:=1 END) AS rec_cnt,
                    (@gru_rec:=recipe_no) AS tmp_rec
                FROM mm_model, 
                     (SELECT 
                            @gru_eqip:='', 
                            @num_eqip:=0, 
                            @gru_cham:='', 
                            @num_cham:=0,
                            @gru_rec:='', 
                            @num_rec:=0) sub
                ORDER BY equipment_id) TEMP
        '''

        #list = mmModel.objects.select_related('dataset').all().order_by('id')

        context = {
            'list': mmModel.objects.raw(sql),
            'equip_list': mmModel.objects.raw(tree_sql)
        }

        return render(request, 'monitoring/monitoringmain.html', context)

class execute_monitoring(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        file_list = os.listdir("AIBIZ/monitoring_anomalies/")
        #csv_list = []

        '''
            with open("AIBIZ/monitoring_anomalies/2020_07_10_0164660_4.csv", "rt") as f :
                reader = csv.reader(f, delimiter = ";")
                for row in reader :
                    csv_list.append(row)
    
            print(csv_list)
        '''

        context = {
            "anomalies_list": file_list
            #"reader" : csv_list
        }

        return JsonResponse(context, content_type='application/json')
