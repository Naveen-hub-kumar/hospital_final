from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor
from django.contrib.auth.models import User
from users.models import UserProfile

#from .forms import PatientForm
from datetime import datetime
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Doctor

from .serializers import DoctorSerializer
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

# ADD DOCTOR

# def add_doctor(request):

#     if request.method == 'POST':

#         name = request.POST.get('name')
#         specialization = request.POST.get('specialization')
#         phone = request.POST.get('phone')

#         Doctor.objects.create(
#             name=name,
#             specialization=specialization,
#             phone=phone
#         )

#         # ✅ FIXED REDIRECT
#         return redirect('doctor_list')

#     return render(request, 'doctors/add_doctor.html')

def add_doctor(request):

    if request.method == 'POST':

        # FORM DATA

        name = request.POST['name']

        specialization = request.POST['specialization']

        phone = request.POST['phone']

        username = request.POST['username']

        password = request.POST['password']

        # CREATE LOGIN USER

        user = User.objects.create_user(
            username=username,
            password=password
        )

        # CREATE ROLE

        UserProfile.objects.create(
            user=user,
            role='doctor'
        )

        # CREATE DOCTOR

        Doctor.objects.create(
            user=user,
            name=name,
            specialization=specialization,
            phone=phone
        )

        return redirect('/doctors/')

    return render(request, 'doctors/add_doctor.html')

def doctor_list(request):

    query = request.GET.get('q')

    if query:
        doctors = Doctor.objects.filter(name__icontains=query)
    else:
        doctors = Doctor.objects.all()

    return render(request,
                  'doctors/doctor_list.html',
                  {'doctors': doctors})
# VIEW DOCTOR

def view_doctor(request, id):

    doctor = get_object_or_404(Doctor, id=id)

    return render(request,
                  'doctors/view_doctor.html',
                  {'doctor': doctor})


# UPDATE DOCTOR

def update_doctor(request, id):

    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':

        doctor.name = request.POST['name']

        doctor.specialization = request.POST['specialization']

        doctor.phone = request.POST['phone']

        doctor.save()

        return redirect('/doctors/')

    return render(
        request,
        'doctors/update_doctor.html',
        {'doctor': doctor}
    )

# DELETE DOCTOR

def delete_doctor(request, id):

    doctor = get_object_or_404(Doctor, id=id)

    doctor.delete()

    return redirect('/doctors/')



class DoctorListCreateAPI(APIView):

    # 🔹 GET all patients
    def get(self, request):
        doctors = Doctor.objects.all()

        serializer = DoctorSerializer(doctors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 CREATE new patient
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# RETRIEVE + UPDATE + DELETE
class DoctorRetrieveUpdateDeleteAPI(APIView):

    # 🔹 GET single patient
    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 UPDATE patient (partial update)
    def patch(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)

        serializer = DoctorSerializer(
            doctor,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 DELETE patient
    def delete(self, request, pk):
        patient = get_object_or_404(Doctor, pk=pk)
        patient.delete()

        return Response(
            {"message": "Patient deleted successfully"},
            status=status.HTTP_200_OK
        )