from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from config.models import mmModel

from django.shortcuts import render, redirect, get_object_or_404

class monitoringmain(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        list = mmModel.objects.all().order_by('id')
        context['list'] = list
        return render(request, 'monitoring/monitoringmain.html', context)
