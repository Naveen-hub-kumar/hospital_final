from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from django.contrib.auth.models import User
from users.models import UserProfile

from .forms import PatientForm
from datetime import datetime
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Patient

from .serializers import PatientSerializer
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.core.paginator import Paginator




def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            # Step 1: Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            # Step 2: Create Patient
            patient = form.save(commit=False)
            patient.user = user
            patient.save()

            return redirect('patient_list')

    else:
        form = PatientForm()

    return render(request, 'patients/add_patient.html', {'form': form})




# ADD PATIENT

# def add_patient(request):

#     if request.method == 'POST':

#         # FORM DATA

#         name = request.POST['name']
#         age = request.POST['age']
#         gender = request.POST['gender']
#         phone = request.POST['phone']
#         address = request.POST['address']

#         # CREATE USERNAME & PASSWORD

#         username = phone
#         password = "patient123"

#         # CREATE DJANGO USER

#         user = User.objects.create_user(
#             username=username,
#             password=password
#         )

#         # CREATE USER ROLE

#         UserProfile.objects.create(
#             user=user,
#             role='patient'
#         )

#         # CREATE PATIENT

#         Patient.objects.create(
#             user=user,
#             name=name,
#             age=age,
#             gender=gender,
#             phone=phone,
#             address=address
#         )

#         return redirect('/patients/')

#     return render(request, 'patients/add_patient.html')
# # PATIENT LIST

def patient_list(request):

    search = request.GET.get('search')

    if search:

        patients = Patient.objects.filter(name__icontains=search)

    else:

        patients = Patient.objects.all()

    return render(
        request,
        'patients/patient_list.html',
        {'patients': patients}
    )
# VIEW PATIENT

def view_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    return render(request,
                  'patients/view_patient.html',
                  {'patient': patient})


# UPDATE PATIENT

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Patient

def update_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == "POST":
        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.gender = request.POST.get("gender")
        patient.phone = request.POST.get("phone")
        patient.address = request.POST.get("address")

        patient.save()  #  SAVE TO DATABASE

        return redirect("patient_list")  # ✅ REDIRECT AFTER UPDATE

    return render(request, "patients/update_patient.html", {"patient": patient})

# DELETE PATIENT


def delete_patient(request, id):

    patient = get_object_or_404(Patient, id=id)
    patient.delete()

    # FIXED REDIRECT (use URL name, NOT hardcoded path)
    return redirect('patient_list')




#=======================API CREATION==============================


class PatientListCreateAPI(APIView):

    #  GET all patients
    def get(self, request):
        patients = Patient.objects.all()

        serializer = PatientSerializer(patients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    #  CREATE new patient
    def post(self, request):
        serializer = PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# RETRIEVE + UPDATE + DELETE
class PatientRetrieveUpdateDeleteAPI(APIView):

    #  GET single patient
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  UPDATE patient (partial update)
    def patch(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)

        serializer = PatientSerializer(
            patient,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  DELETE patient
    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()

        return Response(
            {"message": "Patient deleted successfully"},
            status=status.HTTP_200_OK
        )