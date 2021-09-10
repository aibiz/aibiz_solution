from django.urls import path
from . import views

urlpatterns = [
    # 모델 학습
    # path('/training', training_views.training_main, name='training')
    path('analysis', views.analysis_main.as_view()),
    path('analysis/find_chamber', views.find_chamber.as_view()),
    path('analysis/find_recipe', views.find_recipe.as_view()),
    path('analysis/find_revision', views.find_revision.as_view()),
    path('analysis/find_sensor', views.find_sensor.as_view())
]