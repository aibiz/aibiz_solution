from django.urls import path
from .views import monitoring_views, user_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # 모델 학습
    path('', monitoring_views.MoniterView.as_view(), name='index'),

    # 로그인
    path('login', user_views.LoginView.as_view(), name='login'),
    path('logout-page', user_views.LogoutPageView.as_view(), name='logout-page'),
    path("logout", LogoutView.as_view(next_page='/logout-page'), name="logout"),
]