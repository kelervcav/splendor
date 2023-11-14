from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from appointments.models import Appointment
from treatments.models import Treatment


def treatment_analytics(request):
    most_chosen_treatment = Appointment.objects.values('treatment').annotate(count=Count('treatment')).order_by('-count').first()

    if most_chosen_treatment is not None:
        treatment_id = most_chosen_treatment.get('treatment')
        most_chosen_treatment_instance = get_object_or_404(Treatment, pk=treatment_id)
        context = {'most_chosen_treatment': most_chosen_treatment_instance, 'count': most_chosen_treatment['count']}

    else:
        context = {'most_chosen_treatment': most_chosen_treatment, 'count': 0}

    return render(request, 'treatment_analytics.html', context)
