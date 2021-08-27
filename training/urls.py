from django.urls import path
from . import views

urlpatterns = [
    # 모델 학습
    path('training', views.training_main, name='training')

]