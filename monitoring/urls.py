from django.urls import path
from .views import monitoring_views, user_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # 모델 학습
    #path('', monitoring_views.MoniterView.as_view(), name='index'),




    # Monitoring

    path('monitoring/', monitoring_views.monitoringmain.as_view(), name='monitoringmain')
]