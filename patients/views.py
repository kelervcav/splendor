from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from appointments.forms import BookingAppointmentForm
from appointments.models import Appointment
from patients.forms import RegistrationForm


# Create your views here.


def home(request):
    return render(request, 'patients/home.html')


def patient_create(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        patient = form.save()
        patient.is_patient = True
        patient.save()
        messages.success(request, 'Patient registered successfully.')
        return redirect('patients:patient_create')
    template_name = 'patients/patient_create.html'
    context = {'form': form}
    return render(request, template_name, context)

