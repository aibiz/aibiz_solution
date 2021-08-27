from django.shortcuts import render


def training_main(request):
    context ={}

    return render(request, 'training.html', context)
# Create your views here.
