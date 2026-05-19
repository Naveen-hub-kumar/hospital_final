from django.shortcuts import render, redirect, get_object_or_404

from .models import Appointment

from doctors.models import Doctor

from patients.models import Patient


# BOOK APPOINTMENT

def book_appointment(request):

    doctors = Doctor.objects.all()

    patients = Patient.objects.all()

    if request.method == 'POST':

        doctor_id = request.POST['doctor']

        patient_id = request.POST['patient']

        appointment_date = request.POST['appointment_date']

        doctor = Doctor.objects.get(id=doctor_id)

        patient = Patient.objects.get(id=patient_id)

        Appointment.objects.create(

            doctor=doctor,
            patient=patient,
            appointment_date=appointment_date

        )

        return redirect('/appointments/')

    return render(request,
                  'appointments/book_appointment.html',
                  {
                      'doctors': doctors,
                      'patients': patients
                  })


# APPOINTMENT LIST

def appointment_list(request):

    search = request.GET.get('search')

    if search:
        appointments = Appointment.objects.filter(
            doctor__name__icontains=search
        ) | Appointment.objects.filter(
            patient__name__icontains=search
        )

    else:
        appointments = Appointment.objects.all()

    return render(
        request,
        'appointments/appointment_list.html',
        {'appointments': appointments}
    )

# VIEW APPOINTMENT

def view_appointment(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    return render(request,
                  'appointments/view_appointment.html',
                  {'appointment': appointment})


# UPDATE APPOINTMENT

def update_appointment(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    doctors = Doctor.objects.all()

    patients = Patient.objects.all()

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')

        patient_id = request.POST.get('patient')

        appointment_date = request.POST.get('appointment_date')

        appointment.doctor = Doctor.objects.get(id=doctor_id)

        appointment.patient = Patient.objects.get(id=patient_id)

        appointment.appointment_date = appointment_date

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

# DELETE APPOINTMENT

def delete_appointment(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    appointment.delete()

    return redirect('/appointments/')