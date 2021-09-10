from django.urls import path
from .views import monitoring_views, user_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # 모델 학습
    #path('', monitoring_views.MoniterView.as_view(), name='index'),

    # Monitoring
    path('monitoring/', monitoring_views.monitoringmain.as_view(), name='monitoringmain'),
    path('monitoring/execute', monitoring_views.execute_monitoring.as_view(), name='execute_monitoring'),
    path('monitoring/find_chamber', monitoring_views.find_chamber.as_view(), name='find_chamber'),
    path('monitoring/find_recipe', monitoring_views.find_recipe.as_view(), name='find_recipe'),
    path('monitoring/find_sensor', monitoring_views.find_sensor.as_view(), name='find_sensor'),
    path('monitoring/run_monitoring', monitoring_views.run_monitoring.as_view(), name='run_monitoring'),
    path('monitoring/upload', monitoring_views.monitoring_upload.as_view(), name='monitoring_upload'),
    path('monitoring/stop_thread', monitoring_views.stop_thread.as_view(), name='stop_thread')
]