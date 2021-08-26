from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse

from django.shortcuts import render, redirect, get_object_or_404

class MoniterView(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        context['username'] = request.user.username
        
        return render(request, 'index.html', context)