from django.shortcuts import render, redirect, get_object_or_404



from datetime import datetime
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Appointment

from .serializers import AppointmentSerializer
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

# from .models import Appointment

# from doctors.models import Doctor

# from patients.models import Patient


# # BOOK APPOINTMENT

# def book_appointment(request):

#     doctors = Doctor.objects.all()

#     patients = Patient.objects.all()

#     if request.method == 'POST':

#         doctor_id = request.POST['doctor']

#         patient_id = request.POST['patient']

#         appointment_date = request.POST['appointment_date']

#         doctor = Doctor.objects.get(id=doctor_id)

#         patient = Patient.objects.get(id=patient_id)

#         Appointment.objects.create(

#             doctor=doctor,
#             patient=patient,
#             appointment_date=appointment_date

#         )

#         return redirect('/appointments/')

#     return render(request,
#                   'appointments/book_appointment.html',
#                   {
#                       'doctors': doctors,
#                       'patients': patients
#                   })


# # APPOINTMENT LIST

# def appointment_list(request):

#     search = request.GET.get('search')

#     if search:
#         appointments = Appointment.objects.filter(
#             doctor__name__icontains=search
#         ) | Appointment.objects.filter(
#             patient__name__icontains=search
#         )

#     else:
#         appointments = Appointment.objects.all()

#     return render(
#         request,
#         'appointments/appointment_list.html',
#         {'appointments': appointments}
#     )

# # VIEW APPOINTMENT

# def view_appointment(request, id):

#     appointment = get_object_or_404(Appointment, id=id)

#     return render(request,
#                   'appointments/view_appointment.html',
#                   {'appointment': appointment})


# # UPDATE APPOINTMENT

# def update_appointment(request, id):

#     appointment = get_object_or_404(Appointment, id=id)

#     doctors = Doctor.objects.all()

#     patients = Patient.objects.all()

#     if request.method == 'POST':

#         doctor_id = request.POST.get('doctor')

#         patient_id = request.POST.get('patient')

#         appointment_date = request.POST.get('appointment_date')

#         appointment.doctor = Doctor.objects.get(id=doctor_id)

#         appointment.patient = Patient.objects.get(id=patient_id)

#         appointment.appointment_date = appointment_date

#         appointment.save()

#         return redirect('/appointments/')

#     return render(
#         request,
#         'appointments/update_appointment.html',
#         {
#             'appointment': appointment,
#             'doctors': doctors,
#             'patients': patients
#         }
#     )

# # DELETE APPOINTMENT

# def delete_appointment(request, id):

#     appointment = get_object_or_404(Appointment, id=id)

#     appointment.delete()

#     return redirect('/appointments/')





from django.shortcuts import render, redirect
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient


# ================= APPOINTMENT LIST =================

def appointment_list(request):

    query = request.GET.get('q')

    appointments = Appointment.objects.all()

    if query:

        appointments = appointments.filter(
            doctor__name__icontains=query
        )

    return render(request,
                  'appointments/appointment_list.html',
                  {
                      'appointments': appointments
                  })


# ================= BOOK APPOINTMENT =================

def book_appointment(request):

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == 'POST':

        doctor_id = request.POST['doctor']
        patient_id = request.POST['patient']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']

        doctor = Doctor.objects.get(id=doctor_id)
        patient = Patient.objects.get(id=patient_id)

        # CHECK DUPLICATE

        appointment_exists = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists()

        if appointment_exists:

            return render(
                request,
                'appointments/book_appointment.html',
                {
                    'error': 'Sorry, doctor already appointed.',
                    'doctors': doctors,
                    'patients': patients
                }
            )

        # KEEP THIS CODE HERE ↓↓↓↓↓

        Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        return redirect('/appointments/')

    return render(
        request,
        'appointments/book_appointment.html',
        {
            'doctors': doctors,
            'patients': patients
        }
    )
# ================= VIEW APPOINTMENT =================

def view_appointment(request, id):

    appointment = Appointment.objects.get(id=id)

    return render(
        request,
        'appointments/view_appointment.html',
        {
            'appointment': appointment
        }
    )


# ================= UPDATE APPOINTMENT =================

def update_appointment(request, id):

    appointment = Appointment.objects.get(id=id)

    doctors = Doctor.objects.all()

    patients = Patient.objects.all()

    error = None

    if request.method == 'POST':

        doctor_id = request.POST['doctor']

        patient_id = request.POST['patient']

        appointment_date = request.POST['appointment_date']

        appointment_time = request.POST['appointment_time']

        doctor = Doctor.objects.get(id=doctor_id)

        patient = Patient.objects.get(id=patient_id)

        # CHECK DUPLICATE

        appointment_exists = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exclude(id=id).exists()

        if appointment_exists:

            error = "Sorry, this doctor already has an appointment at this time."

            return render(
                request,
                'appointments/update_appointment.html',
                {
                    'appointment': appointment,
                    'doctors': doctors,
                    'patients': patients,
                    'error': error
                }
            )

        # UPDATE DATA

        appointment.doctor = doctor

        appointment.patient = patient

        appointment.appointment_date = appointment_date

        appointment.appointment_time = appointment_time

        appointment.save()

        return redirect('/appointments/')

    return render(
        request,
        'appointments/update_appointment.html',
        {
            'appointment': appointment,
            'doctors': doctors,
            'patients': patients
        }
    )


# ================= DELETE APPOINTMENT =================

def delete_appointment(request, id):

    appointment = Appointment.objects.get(id=id)

    appointment.delete()

    return redirect('/appointments/')







#================================API CREATION===========================


class AppointmentListCreateAPI(APIView):

    #  GET all patients
    # class AppointmentListCreateAPI(APIView):

    def get(self, request):

        appointments = Appointment.objects.all()

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)
    #  CREATE new patient
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# RETRIEVE + UPDATE + DELETE
class AppointmentRetrieveUpdateDeleteAPI(APIView):

    #  GET single appointment
    def get(self, request, pk):

        appointment = get_object_or_404(
            Appointment,
            pk=pk
        )

        serializer = AppointmentSerializer(appointment)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    #  UPDATE appointment
    def patch(self, request, pk):

        appointment = get_object_or_404(
            Appointment,
            pk=pk
        )

        serializer = AppointmentSerializer(
            appointment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE appointment
    def delete(self, request, pk):

        appointment = get_object_or_404(
            Appointment,
            pk=pk
        )

        appointment.delete()

        return Response(
            {
                "message": "Appointment deleted successfully"
            },
            status=status.HTTP_200_OK
        )