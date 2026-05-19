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

]