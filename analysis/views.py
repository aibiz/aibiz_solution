from django.shortcuts import render

def analysis_main(request):
    context = {}
    return render(request, "analysis.html", context)

