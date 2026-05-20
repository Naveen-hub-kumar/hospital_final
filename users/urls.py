from django.urls import path

from .views import *

urlpatterns = [

    path('', login_view),

    path(
        'admin-dashboard/',
        admin_dashboard
    ),

    path(
        'patient-dashboard/',
        patient_dashboard
    ),

    path(
        'logout/',
        logout_view
    ),

path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),

path('doctor-appointments/', doctor_appointments, name='doctor_appointments'),

path('doctor-patients/', doctor_patients, name='doctor_patients'),

]