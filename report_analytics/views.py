from django.shortcuts import render
from appointments.models import Appointment


# Create your views here.

def report_analytics(request):
    most_availed_treatment = Appointment.objects.get('treatment')

    template_name = 'report_analytics.html'
    context = {
        'most_availed_treatment': most_availed_treatment,
    }
    return render(request, template_name, context)
