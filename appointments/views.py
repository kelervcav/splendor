from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import BookingAppointmentForm
from .models import Appointment
from treatments.models import Treatment
from django.utils import timezone

User = get_user_model()


# Create your views here.
def appointment_create(request):
    form = BookingAppointmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_info')
    context = {'form': form}
    return render(request, 'appointments/appointment_create.html', context)


def appointment_edit(request, pk):
    set_appointment = get_object_or_404(Appointment, id=pk)
    form = BookingAppointmentForm(request.POST or None, instance=set_appointment)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Appointment updated successfully.')
        return redirect('appointments:appointment_info')
    template_name = 'appointments/appointment_edit.html'
    context = {'set_appointment': set_appointment, 'form': form}
    return render(request, template_name, context)


def appointment_delete(request, pk):
    set_appointment = get_object_or_404(Appointment, id=pk)
    set_appointment.status = 'Canceled'
    set_appointment.save()
    messages.success(request,
                     'Appointment has been marked as cancelled.')
    return redirect('appointments:appointment_list')


# for therapist
def appointment_list(request):
    appointment_list = Appointment.objects.all()
    template_name = 'appointments/appointment_list.html'
    context = {'appointment_list': appointment_list}
    return render(request, template_name, context)


def appointment_info(request):
    appointment_info = Appointment.objects.all()
    template_name = 'appointments/appointment_info.html'
    context = {'appointment_info': appointment_info}
    return render(request, template_name, context)

