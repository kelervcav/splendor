from django.shortcuts import render, redirect
from .forms import BookingAppointmentForm
from appointments.models import Appointment

# Create your views here.


def home(request):
    return render(request, 'patients/home.html')


def appointment_info(request):
    appointment_info = Appointment.objects.all()
    print(appointment_info.query)
    template_name = 'patients/appointment_info.html'
    context = {'appointment_info': appointment_info}
    return render(request, template_name, context)


def appointment_create(request):
    form = BookingAppointmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('patients:appointment_info')
    context = {'form': form}
    return render(request, 'patients/appointment_create.html', context)
