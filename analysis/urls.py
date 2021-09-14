from django.urls import path
from . import views

urlpatterns = [
    # 모델 학습
    # path('/training', training_views.training_main, name='training')
    path('analysis', views.analysis_main.as_view()),
]