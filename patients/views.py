from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from django.contrib.auth.models import User
from users.models import UserProfile

from .forms import PatientForm



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

def update_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':

        patient.name = request.POST['name']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.phone = request.POST['phone']
        patient.address = request.POST['address']

        patient.save()

        return redirect('/patients/list/')

    return render(request,
                  'patients/update_patient.html',
                  {'patient': patient})


# DELETE PATIENT

def delete_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    patient.delete()

    return redirect('/patients/list/')