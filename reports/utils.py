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


