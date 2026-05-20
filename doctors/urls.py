from django.urls import path
from .views import *

urlpatterns = [

    path('add/', add_doctor, name='add_doctor'),

    path('', doctor_list, name='doctor_list'),

    path('view/<int:id>/', view_doctor, name='view_doctor'),

    path('update/<int:id>/', update_doctor, name='update_doctor'),

    path('delete/<int:id>/', delete_doctor, name='delete_doctor'),

     path(

        'api/',

        DoctorListCreateAPI.as_view(),

        name='doctor_api'

     ),


    # #  path(

    # #     'api/<int:pk>/',

    # #     DoctorRetrieveUpdateDeleteAPI.as_view(),

    # #     name='doctor_detail_api'

    # ),
    path('api/<int:pk>/', DoctorRetrieveUpdateDeleteAPI.as_view(),name='doctor_update_api'),


]