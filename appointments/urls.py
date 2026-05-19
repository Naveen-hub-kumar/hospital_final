from django.urls import path
from .views import *

urlpatterns = [

    path('book/', book_appointment, name='book_appointment'),

    path('',appointment_list, name='appointment_list'),

    path('view/<int:id>/', view_appointment, name='view_appointment'),

    path('update/<int:id>/', update_appointment, name='update_appointment'),

    path('delete/<int:id>/', delete_appointment, name='delete_appointment'),

]