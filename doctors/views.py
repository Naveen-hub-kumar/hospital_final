from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor


# ADD DOCTOR

def add_doctor(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        phone = request.POST.get('phone')

        Doctor.objects.create(
            name=name,
            specialization=specialization,
            phone=phone
        )

        # ✅ FIXED REDIRECT
        return redirect('doctor_list')

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

    return redirect('/doctors/list/')