from django.urls import path
from .views import problemmain, problemadd, insertproblem

app_name = "problem"

urlpatterns = [
    path('problem/', problemmain, name="problemmain"),
    path('problemadd/', problemadd, name="problemadd"),
    path('insertproblem/', insertproblem, name="insertproblem")
]