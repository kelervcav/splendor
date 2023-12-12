from datetime import time, datetime, date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from pusher import Pusher

from treatments.models import Service, Treatment
from user_profile.decorators import admin_required
from .forms import BookingAppointmentForm
from .models import Appointment


User = get_user_model()

# Create your views here.

pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
)


# for patients

@login_required
def appointment_create(request):

    services = Service.objects.filter(is_active=True)
    form = BookingAppointmentForm()
    if request.method == 'POST':
        form = BookingAppointmentForm(request.POST or None)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user

            appointment_date = form.cleaned_data['date']
            appointment_time = form.cleaned_data['time']

            # Check if the user already has an appointment at the same date and time
            existing_appointment = Appointment.objects.filter(
                user=request.user,
                date=appointment_date,
                time=appointment_time
            ).exists()

            if existing_appointment:
                form.add_error('time', 'You already have an appointment at this time and date.')
                # Return the form with an error message
                return render(request, 'appointments/appointment_create.html', {'form': form, 'services': services})
            appointment.save()

            # pusher notification
            appointment_datetime = datetime.combine(appointment_date, datetime.strptime(appointment_time, '%H:%M:%S').time())
            formatted_datetime = appointment_datetime.strftime("%m/%d/%Y at %I:%M %p")
            data = {'message': f"{appointment.user.first_name} booked an appointment for {formatted_datetime}"}
            pusher.trigger('splendor-channel', 'my-event', data)

            return redirect('appointments:appointment_info')

    context = {'form': form, 'services': services}
    return render(request, 'appointments/appointment_create.html', context)


@login_required
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


@login_required
def appointment_cancel(request, pk):
    set_appointment = get_object_or_404(Appointment, id=pk)
    set_appointment.is_cancel = True
    set_appointment.save()
    return redirect('appointments:appointment_info')


# for therapist
@login_required
@admin_required
@permission_required('appointments.approve_appointment', raise_exception=True)
def approve_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.is_approved = True
    appointment.save()
    messages.success(request,
                     'Appointment has been approved.')
    return redirect('appointments:appointment_list')


@login_required
@admin_required
@permission_required('appointments.approve_appointment', raise_exception=True)
def complete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.is_completed = True
    appointment.save()
    messages.success(request,
                     'Appointment has been completed.')
    return redirect('appointments:appointment_list')


# for therapist
@login_required
@admin_required
@permission_required('appointments.view_appointment', raise_exception=True)
def appointment_list(request):
    date_now = timezone.now()
    appointment_list = Appointment.objects.all().order_by('-created_at')
    template_name = 'appointments/appointment_list.html'
    context = {'appointment_list': appointment_list, 'date_now': date_now}
    print(date_now)
    return render(request, template_name, context)


@login_required
def appointment_info(request):
    user = request.user
    appointment_info = Appointment.objects.filter(user=user).order_by('-created_at')
    services = Service.objects.filter(is_active=True)
    template_name = 'appointments/appointment_info.html'
    context = {'appointment_info': appointment_info, 'services': services}
    return render(request, template_name, context)

