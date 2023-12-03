from user_profile.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404

from appointments.models import Appointment
from treatments.models import Treatment


def most_availed_treatment(date_from, date_to):
    result = (
        Appointment.objects
        .filter(date__range=[date_from, date_to], is_approved=True)
        .values('treatment')
        .annotate(count=Count('treatment'))
    )
    for treatment in result:
        treatment_id = treatment.get('treatment')
        treatment_instance = get_object_or_404(Treatment, pk=treatment_id)
        treatment['treatment_name'] = treatment_instance.name

    return result


def get_patients(date_from, date_to):
    patients = (User.objects
                .filter(is_patient=True, created_at__range=[date_from, date_to])
                .order_by('created_at')
                .select_related('userprofile'))

    return patients


def get_treatments(date_from, date_to):
    treatments = (Treatment.objects
                  .filter(created_at__range=[date_from, date_to])
                  .order_by('created_at'))

    return treatments
