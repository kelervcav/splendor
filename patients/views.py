from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from patients.forms import RegistrationForm, CustomRegistration, MembershipRenewalForm
from redeem_points.models import RedeemPoints
from transactions.models import Transaction
from user_profile.decorators import admin_required
from user_profile.forms import AdminEditPasswordForm
from user_profile.models import UserProfile

User = get_user_model()


# Create your views here.
@login_required
@admin_required
@permission_required('patients.view_offer', raise_exception=True)
def patient_list(request):
    patients_list = User.objects.filter(is_patient=True).order_by('-created_at')
    template_name = 'patients/patient_list.html'
    context = {'patients_list': patients_list}
    return render(request, template_name, context)


@login_required
@admin_required
def patient_create(request):
    registration_form = RegistrationForm(request.POST or None)
    custom_form = CustomRegistration(request.POST or None)

    if registration_form.is_valid() and custom_form.is_valid():
        registration = registration_form.save(commit=False)
        registration.is_patient = True
        registration.set_custom_password()
        registration.save()
        user = User.objects.get(id=registration.id)
        user.generate_qr()
        user.save()
        gender = custom_form.save(commit=False)
        gender.user = registration
        gender.save()
        messages.success(request, 'Patient registered successfully.')
        return redirect('patients:patient_list')

    template_name = 'patients/patient_create.html'
    context = {'registration_form': registration_form, 'custom_form': custom_form}
    return render(request, template_name, context)


# for therapist
@login_required
@admin_required
def patient_info(request, pk):
    patient_info = User.objects.filter(id=pk)
    transactions = Transaction.objects.filter(user=pk).order_by('-date_added')
    total_points = UserProfile.objects.filter(user=pk)
    redeemed_list = RedeemPoints.objects.filter(user=pk).order_by('-date_redeemed')
    date_now = datetime.now()
    template_name = 'patients/patient_info.html'
    context = {'patient_info': patient_info,
               'transactions': transactions,
               'total_points': total_points,
               'redeemed_list': redeemed_list,
               'date_now': date_now}
    return render(request, template_name, context)


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(User, id=pk)
    registration_form = RegistrationForm(request.POST or None, instance=patient)
    custom_form = CustomRegistration(request.POST or None, instance=patient.userprofile)
    if registration_form.is_valid() and custom_form.is_valid():
        registration = registration_form.save(commit=False)
        registration.is_patient = True
        registration.save()
        gender = custom_form.save(commit=False)
        gender.user = registration
        gender.save()
        messages.success(request, 'Patient has been edited successfully.')
        return redirect('patients:patient_edit', pk)
    template_name = 'patients/patient_edit.html'
    context = {'registration_form': registration_form, 'patient': patient, 'custom_form': custom_form}
    return render(request, template_name, context)


@login_required
def patient_disable(request, pk):
    patients = get_object_or_404(User, id=pk)
    patients.is_active = False
    patients.save()
    messages.success(request, 'Patient has been disabled.')
    return redirect('patients:patient_list')


def patient_renewal(request, pk):
    patient = get_object_or_404(User, id=pk)
    user_profile = UserProfile.objects.get(user=patient)
    form = MembershipRenewalForm(request.POST or None, instance=patient)
    if form.is_valid():
        renewal = form.save()
        renewal.save()
        renewal_duration = timedelta(days=365)
        new_expiry_date = user_profile.account_expiry + renewal_duration
        user_profile.account_expiry = new_expiry_date
        user_profile.save()
        messages.success(request, 'User membership account successfully renewed.')
        return redirect('patients:patient_info', pk)

    template_name = 'patients/patient_renewal.html'
    context = {'form': form, 'patient': patient}
    return render(request, template_name, context)


@login_required
@admin_required
def reset_password(request, pk):
    patient = get_object_or_404(User, id=pk)
    template_name = 'patients/patient_reset_password.html'
    context = {'patient': patient}
    return render(request, template_name, context)


@login_required
@admin_required
def generate_password(request, pk):
    patient = get_object_or_404(User, id=pk)
    generated_password = request.POST.get('password')
    print(generated_password)
    patient.set_password(generated_password)
    patient.save()
    messages.success(request, 'Password reset successfully.')
    return redirect('patients:patient_edit', pk)


# patient UI
@login_required
def patient_profile(request, pk):
    patient_info = User.objects.get(id=pk)
    patient = get_object_or_404(User, id=request.user.id)
    form = RegistrationForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('patients:patient_profile')

    template_name = 'patients/patient_profile.html'
    context = {'form': form, 'patient': patient, 'patient_info': patient_info}
    return render(request, template_name, context)


# patient UI
@login_required
def change_password(request):
    patient = get_object_or_404(User, id=request.user.id)
    form = AdminEditPasswordForm(data=request.POST or None, user=patient)
    if form.is_valid():
        form.save()
        return redirect('/')

    template_name = 'patients/patient_change_password.html'
    context = {'form': form}
    return render(request, template_name, context)