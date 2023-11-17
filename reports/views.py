from datetime import timedelta

from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from appointments.models import Appointment
from treatments.models import Treatment

from django.shortcuts import render
from django.utils import timezone


# Create your views here.

def report(request):
    most_chosen_treatment = Appointment.objects.values('treatment').annotate(treatment_count=Count('treatment'))

    treatment_data = []
    treatment_label = []
    for treatment in most_chosen_treatment:
        treatment_id = treatment.get('treatment')
        treatment_instance = get_object_or_404(Treatment, pk=treatment_id)

        treatment_data.append(treatment['treatment_count'])
        treatment_label.append(str(treatment_instance))

    template_name = 'reports.html'
    context = {
        'treatment_data': treatment_data,
        'treatment_label': treatment_label,

    }
    return render(request, template_name, context)


def weekly_report(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)
    result = report(start_date, end_date)
    return render(request, 'report.html', {'result': result})

#
# def monthly_report(request):
#     end_date = timezone.now().date()
#     start_date = end_date - timedelta(days=30)
#     result = report(start_date, end_date)
#     return render(request, 'report.html', {'result': result})
#
#
# def daily_report(request):
#     end_date = timezone.now().date()
#     start_date = end_date - timedelta(days=1)
#     result = report(start_date, end_date)
#     return render(request, 'report.html', {'result': result})
