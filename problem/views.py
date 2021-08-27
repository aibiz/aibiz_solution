from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from config.models import mmProblem
import time

def problemmain(request) :
 
    query = '''
    SELECT *, SUBSTR(problem_name, 1, 1) first
    FROM mm_problem
    '''

    context = {
        'problemContent' : mmProblem.objects.raw(query)
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

def problemsend(request) :
    context = {
        'problem_Id' : request.GET['problem_Id'],
        'problem_Name' : request.GET['problem_Name'],
    }

    return render(request, 'problem/problemsend.html', context)


