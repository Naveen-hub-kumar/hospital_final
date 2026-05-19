from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import UserProfile

from doctors.models import Doctor
from patients.models import Patient

from django.contrib.auth.decorators import login_required
from appointments.models import Appointment



def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            profile, created = UserProfile.objects.get_or_create(
            user=user,
       defaults={'role': 'patient'}
)
        
        if profile.role == 'admin':

             return redirect('/admin-dashboard/')

        else:

                return redirect('/patient-dashboard/')

    return render(request,'users/login.html')


def logout_view(request):

    logout(request)

    return redirect('/')

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