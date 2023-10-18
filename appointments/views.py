from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import BookingForm
from .models import Appointment
from services.models import Treatment
from django.utils import timezone


# Create your views here.

def appointment_edit(request, pk):
    set_appointment = get_object_or_404(Appointment, id=pk)
    form = BookingForm(request.POST or None, instance=set_appointment)
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
