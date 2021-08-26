from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('uploaddata', views.DataUploadView.as_view(), name='uploaddata'),
]