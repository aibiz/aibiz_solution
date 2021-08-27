from django.urls import path
from .views import problemmain, problemadd, insertproblem, problemsend

app_name = "problem"

urlpatterns = [
    path('problem/', problemmain, name="problemmain"),
    path('problem/problemadd/', problemadd, name="problemadd"),
    path('insertproblem/', insertproblem, name="insertproblem"),
    path('problem/problemsend/', problemsend, name="problemsend")
]