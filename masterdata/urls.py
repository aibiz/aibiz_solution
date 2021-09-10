from django.urls import path
from . import views

urlpatterns = [
    path('master/', views.masterdatamain.as_view(), name='mastermain'),
    path('master/recipefind', views.masterdatarecipefind.as_view(), name='mastermainrecipefind'),
    path('master/problemfind', views.masterdataproblemfind.as_view(), name='mastermainproblemfind'),
    path('master/datasetfind', views.masterdatadatasetfind.as_view(), name='mastermaindatasetfind'),
    #mm_model
    path('master/equipmodify', views.equipmentdatamodify.as_view(), name='equipmodify'),
    path('master/updateequip', views.update_equipment.as_view(), name='updateequip'),
    #mm_problem
    path('master/problemmodify', views.problemdatamodify.as_view(), name='problemmodify'),
    path('master/updateproblem', views.update_problem.as_view(), name='updateproblem'),
    path('master/deleteproblem', views.delete_problem.as_view(), name='deleteproblem'),
    #mm_dataset
    path('master/datasetmodify', views.datasetdatamodify.as_view(), name='datasetmodify'),
    path('master/updatedataset', views.update_dataset.as_view(), name='updatedataset'),
    path('master/deletedataset', views.delete_dataset.as_view(), name='deletedataset')
]