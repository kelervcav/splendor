from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from appointments.models import Appointment
from treatments.models import Service, Treatment
from user_profile.decorators import admin_required
from user_profile.models import User
from django.shortcuts import render, get_object_or_404
from django.db.models import Count


@login_required
@admin_required
def dashboard(request):
    now = datetime.now()
    appointment_list = Appointment.objects.filter(date=now.date()).order_by('-created_at')
    service_count = Service.objects.exclude(is_active=False).count()
    treatment_count = Treatment.objects.exclude(is_active=False).count()
    patient_count = User.objects.filter(is_patient=True).count()
    appointment_count = Appointment.objects.filter(date=now.date(), is_approved=True).count()

    # treatment_analytics
    most_chosen_treatment = Appointment.objects.values('treatment').annotate(treatment_count=Count('treatment'))

    treatment_data = []
    treatment_label = []
    for treatment in most_chosen_treatment:
        treatment_id = treatment.get('treatment')
        treatment_instance = get_object_or_404(Treatment, pk=treatment_id)

        treatment_data.append(treatment['treatment_count'])
        treatment_label.append(str(treatment_instance))

    template_name = 'dashboard.html'
    context = {
        'appointment_list': appointment_list,
        'transactions': 'test',
        'service_count': service_count,
        'treatment_count': treatment_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'treatment_data': treatment_data,
        'treatment_label': treatment_label,

    }
    return render(request, template_name, context)

