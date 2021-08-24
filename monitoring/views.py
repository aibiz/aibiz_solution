from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404

class MoniterView(TemplateView):
    template_name = 'monitering/test.html'