from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from appointments.models import Appointment
from treatments.models import Treatment


def treatment_analytics(request):
    most_chosen_treatment = Appointment.objects.values('treatment').annotate(treatment_count=Count('treatment'))

    treatment_data = []
    treatment_label = []
    for treatment in most_chosen_treatment:
        treatment_id = treatment.get('treatment')
        treatment_instance = get_object_or_404(Treatment, pk=treatment_id)

        treatment_data.append(treatment['treatment_count'])
        treatment_label.append(str(treatment_instance))

    return render(request, 'treatment_analytics.html',
                  {'treatment_data': treatment_data,
                   'treatment_label': treatment_label})
