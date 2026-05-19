from django.urls import path
from .views import *

urlpatterns = [

    path('add/', add_patient, name='add_patient'),


    # path('list/', patient_list, name='patient_list'),

    path('', patient_list, name='patient_list'),

    path('view/<int:id>/', view_patient, name='view_patient'),

    path('update/<int:id>/', update_patient, name='update_patient'),

    path('delete/<int:id>/', delete_patient, name='delete_patient'),

]