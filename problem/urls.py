from django.urls import path
<<<<<<< HEAD
from .views import problemmain, problemadd, insertproblem

app_name = "problem"

urlpatterns = [
    path('', problemmain, name="problemmain"),
    path('problemadd/', problemadd, name="problemadd"),
    path('insertproblem/', insertproblem, name="insertproblem")
]