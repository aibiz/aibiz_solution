import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

class LoginView(View):

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, 'user/login.html', context)

class LogoutPageView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, 'user/logout.html', context)

class RegisterView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, 'user/register.html', context)
