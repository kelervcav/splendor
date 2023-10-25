from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from appointments.models import Appointment
from treatments.models import Service, Treatment
from user_profile.decorators import admin_required
from user_profile.models import User
from appointments import views


@login_required
@admin_required
def dashboard(request):
    service_count = Service.objects.exclude(is_active=False).count()
    treatment_count = Treatment.objects.exclude(is_active=False).count()
    patient_count = User.objects.filter(is_patient=True).count()
    appointment_list = Appointment.objects.all()
    template_name = 'dashboard.html'
    context = {
        'transactions': 'test',
        'service_count': service_count,
        'treatment_count': treatment_count,
        'patient_count': patient_count,
        'appointment_list': appointment_list,

    }
    return render(request, template_name, context)

@admin_required
def approve_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.is_approved = True
    appointment.save()
    messages.success(request,
                     'Appointment has been approved.')
    return redirect('appointments:appointment_list')
