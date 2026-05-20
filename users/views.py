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