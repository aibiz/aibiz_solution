from django.urls import path
from . import views

urlpatterns = [
    path('master/', views.masterdatamain.as_view(), name='mastermain'),
    path('master/equipfind', views.masterdataequipfind.as_view(), name='mastermainequipfind'),
    path('master/problemfind', views.masterdataproblemfind.as_view(), name='mastermainproblemfind'),
    path('master/datasetfind', views.masterdatadatasetfind.as_view(), name='mastermaindatasetfind'),
    path('master/equipmodify', views.equipmentdatamodify.as_view(), name='equipmodify')
]