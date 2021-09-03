from django.urls import path
from . import views

urlpatterns = [
    # 모델 학습
    path('training', views.training_main, name='training'),
    path('training/start', views.start_training),
    path('training/graphing', views.graphing_training)
]