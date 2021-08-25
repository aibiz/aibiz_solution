from django.urls import path
from .views import monitoring_views, user_views

urlpatterns = [
    # 모델 학습
    path('', monitoring_views.MoniterView.as_view(), name='index'),

    # 로그인
    path('login', user_views.LoginView.as_view(), name='login'),

]