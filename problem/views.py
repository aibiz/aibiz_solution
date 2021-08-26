from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from config.models import mmProblem
import time

def problemmain(request) :
    context = {
        'problemContent' : mmProblem.objects.all()
    }

    return render(request, 'problem/problemmain.html', context)

def problemadd(request) :
    context = {}

    return render(request, 'problem/problemadd.html', context)

def insertproblem(request: HttpRequest) :
    context = {}
    problem_name = request.POST['problem_name']
    problem_note = request.POST['problem_note']

    mmProblem.objects.create(problem_name=problem_name, problem_note=problem_note)

    context['success'] = True
    context['message'] = '등록 되었습니다.'
    return JsonResponse(context, content_type='application/json')

