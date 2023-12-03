
from django.contrib.auth.decorators import login_required, permission_required

from reports.forms import AppointmentDateRangeForm, PatientDateRangeForm, TreatmentDateRangeForm, CancelDateRangeForm, \
    SalesDateRangeForm
from django.shortcuts import render

from reports.utils import most_availed_treatment, get_patients, get_treatments, get_canceled_appointment, \
    total_sales_report
from user_profile.decorators import admin_required

from django.contrib.auth.models import User

# Create your views here.


@login_required
@admin_required
@permission_required('user_profile.view_user', raise_exception=True)
def report(request):
    return render(request, 'reports.html')


def appointment_report(request):
    form = AppointmentDateRangeForm(request.POST or None)
    if form.is_valid():
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        result = most_availed_treatment(date_from, date_to)
        return render(request, 'generate_report.html', {'form': form, 'result': result})

    return render(request, 'reports.html', {'form': form})


def patient_list_report(request):
    form = PatientDateRangeForm(request.POST or None)
    if form.is_valid():
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        patients = get_patients(date_from, date_to)
        return render(request, 'patient_list_report.html', {'form': form, 'patients': patients})

    return render(request, 'reports.html', {'form': form})


def treatment_list_report(request):
    form = TreatmentDateRangeForm(request.POST or None)
    if form.is_valid():
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        treatments = get_treatments(date_from, date_to)
        return render(request, 'treatment_list_report.html', {'form': form, 'treatments': treatments})

    return render(request, 'reports.html', {'form': form})


def canceled_appointment_report(request):
    form = CancelDateRangeForm(request.POST or None)
    if form.is_valid():
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        canceled_appointment = get_canceled_appointment(date_from, date_to)
        return render(request, 'canceled_appointment_list_report.html', {'form': form, 'canceled_appointment': canceled_appointment})

    return render(request, 'reports.html', {'form': form})


def total_sales(request):
    form = SalesDateRangeForm(request.POST or None)
    if form.is_valid():
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        total_sales = total_sales_report(date_from, date_to)
        return render(request, 'total_sales_report.html', {'form': form, 'total_sales': total_sales})

    return render(request, 'reports.html', {'form': form})



