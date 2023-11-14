from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from appointments.models import Appointment
from treatments.models import Service, Treatment
from user_profile.decorators import admin_required
from user_profile.models import User


@login_required
@admin_required
def dashboard(request):
    now = timezone.now()
    appointment_list = Appointment.objects.filter(created_at__date=now.date()).order_by('-created_at')
    service_count = Service.objects.exclude(is_active=False).count()
    treatment_count = Treatment.objects.exclude(is_active=False).count()
    patient_count = User.objects.filter(is_patient=True).count()
    appointment_count = Appointment.objects.filter(created_at__date=now.date()).count()
    template_name = 'dashboard.html'
    context = {
        'appointment_list': appointment_list,
        'transactions': 'test',
        'service_count': service_count,
        'treatment_count': treatment_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,

    }
    return render(request, template_name, context)
