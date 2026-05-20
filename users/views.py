from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import UserProfile
from datetime import date
from doctors.models import Doctor
from patients.models import Patient

from django.contrib.auth.decorators import login_required
from appointments.models import Appointment

from django.shortcuts import get_object_or_404

from .serializers import UserSerializer
#from .decorators import admin_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
User.objects.all()



def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        # AUTHENTICATE USER

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # IF USER EXISTS

        if user is not None:

            login(request, user)

            # GET USER PROFILE

            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'patient'}
            )

            # ROLE BASED REDIRECT

            if profile.role == 'admin':

                return redirect('/admin-dashboard/')

            elif profile.role == 'doctor':

                return redirect('/doctor-dashboard/')

            elif profile.role == 'patient':

                return redirect('/patient-dashboard/')

            else:

                return redirect('/')

        else:

            return render(request, 'users/login.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'users/login.html')


@login_required
def admin_dashboard(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role != 'admin':
        return redirect('/')

    doctors = Doctor.objects.all()

    patients = Patient.objects.all()

    appointments = Appointment.objects.all()

    context = {

        'doctors': doctors,
        'patients': patients,
        'appointments': appointments

    }

    return render(request,
                  'users/admin_dashboard.html',
                  context)

@login_required
def patient_dashboard(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role != 'patient':
        return redirect('/')

    patient = Patient.objects.get(user=request.user)

    appointments = Appointment.objects.filter(patient=patient)

    context = {

        'role': profile.role,
        'patient': patient,
        'appointments': appointments

    }

    return render(request,
                  'patients/patient_dashboard.html',
                  context)



@login_required
def doctor_dashboard(request):

    user_role = UserProfile.objects.get(user=request.user)

    if user_role.role != 'doctor':
        return redirect('/')

    doctor = Doctor.objects.get(user=request.user)

    appointments = Appointment.objects.filter(doctor=doctor)

    # today_appointments = appointments.filter(date=date.today())
    today_appointments = appointments.filter(
    appointment_date=date.today()
)

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'today_appointments': today_appointments,
    }

    return render(request, 'doctors/dashboard.html', context)


@login_required
def doctor_appointments(request):

    doctor = Doctor.objects.get(user=request.user)

    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctors/doctor_appointments.html', {
        'appointments': appointments
    })



@login_required
def doctor_patients(request):

    doctor = Doctor.objects.get(user=request.user)

    appointments = Appointment.objects.filter(doctor=doctor)

    patient_ids = appointments.values_list('patient_id', flat=True)

    patients = Patient.objects.filter(id__in=patient_ids)

    return render(request, 'doctors/doctor_patients.html', {
        'patients': patients
    })

def logout_view(request):

    logout(request)

    return redirect('/')




#=====================API CREATION ========================

class UserListCreateAPI(APIView):

    #  GET all users
    def get(self, request):

        users = UserProfile.objects.all()

        serializer = UserSerializer(
            users,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    #  CREATE new user
    def post(self, request):

        serializer = UserSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserRetrieveUpdateDeleteAPI(APIView):

    #  GET single user
    def get(self, request, pk):

        user = UserProfile.objects.get(pk=pk)

        serializer = UserSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # UPDATE user
    def patch(self, request, pk):

        user = UserProfile.objects.get(pk=pk)

        serializer = UserSerializer(
            user,
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

    # DELETE user
    def delete(self, request, pk):

        user = UserProfile.objects.get(pk=pk)

        user.delete()

        return Response(
            {
                "message": "User deleted successfully"
            },
            status=status.HTTP_200_OK
        )




























#API CREATION FOR Teacher
# class UserListCreationAPI(APIView):
#         def get(self, request):
#                 teachers=UserProfile.objects.all()
#                 serializer=UserSerializer(teachers,many=True)
#                 return Response(serializer.data,status=status.HTTP_200_OK)
        
#         # def post(self,request):
        #         serializer=UserSerializer(data=request.data)
        #         if serializer.is_valid():
        #                 serializer.save()
        #                 return Response(serializer.data,status=status.HTTP_201_CREATED)
        #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # def post(self, request):
        #  user_id = request.data.get("user")

        #     if UserProfile.objects.filter(user_id=user_id).exists():
        #              return Response(
        #                   {"error": "UserProfile already exists for this user"},
        #           status=400
        #         )

        #      serializer = UserSerializer(data=request.data)

        #        if serializer.is_valid():
        #             serializer.save()
        #         return Response(serializer.data, status=201)

        #     return Response(serializer.errors, status=400)