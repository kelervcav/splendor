from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from appointments.models import Appointment
from treatments.models import Service, Treatment
from user_profile.models import User

@login_required
def dashboard(request):
    service_count = Service.objects.exclude(status='Deleted').count()
    treatment_count = Treatment.objects.exclude(status='Deleted').count()
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

