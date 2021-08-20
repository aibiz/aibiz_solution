from django.urls import path
from .views import *

urlpatterns = [
    # 모델 학습
    path('', MoniterView.as_view(), name='moniter')
]