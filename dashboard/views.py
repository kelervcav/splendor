from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import Service, Treatment


@login_required
def dashboard(request):
    total_services = Service.objects.exclude(status='Deleted').count()
    total_treatments = Treatment.objects.exclude(status='Deleted').count()
    template_name = 'dashboard.html'
    context = {
        'transactions': 'test',
        'total_services': total_services,
        'total_treatments': total_treatments,

    }
    return render(request, template_name, context)

