from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from user_profile.decorators import admin_required
from .forms import ServiceForm, TreatmentForm
from .models import Service, Treatment
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
@login_required
@admin_required
@permission_required('treatments.view_service', raise_exception=True)
def service_list(request):
    service_list = Service.objects.all().order_by('-created_at')
    template_name = 'treatments/service_list.html'
    context = {'service_list': service_list}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.add_service', raise_exception=True)
def service_create(request):
    form = ServiceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Service created successfully.')
        return redirect('treatments:service_list')
    template_name = 'treatments/service_create.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.change_service', raise_exception=True)
def service_edit(request, pk):
    service = get_object_or_404(Service, id=pk)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Service updated successfully.')
        return redirect('treatments:service_edit',pk)
    template_name = 'treatments/service_edit.html'
    context = {'service': service, 'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.disable_service', raise_exception=True)
def service_disable(request, pk):
    service = get_object_or_404(Service, id=pk)
    service.is_active = False
    service.save()
    messages.success(request,
                     'Service has been marked as inactive.')
    return redirect('treatments:service_list')


@login_required
@admin_required
@permission_required('treatments.view_treatment', raise_exception=True)
def treatment_list(request):
    treatment_list = Treatment.objects.all().order_by('-created_at')
    template_name = 'treatments/treatment_list.html'
    context = {'treatment_list': treatment_list}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.add_treatment', raise_exception=True)
def treatment_create(request):
    form = TreatmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Treatment created successfully.')
        return redirect('treatments:treatment_list')
    template_name = 'treatments/treatment_create.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.change_treatment', raise_exception=True)
def treatment_edit(request, pk):
    treatment = get_object_or_404(Treatment, id=pk)
    form = TreatmentForm(request.POST or None, instance=treatment)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Treatment created successfully.')
        return redirect('treatments:treatment_edit', pk)
    template_name = 'treatments/treatment_edit.html'
    context = {'form': form, 'treatment': treatment}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.disable_treatment', raise_exception=True)
def treatment_disable(request, pk):
    treatment = get_object_or_404(Treatment, id=pk)
    treatment.is_active = False
    treatment.save()
    messages.success(request,
                     'Treatment has been marked as inactive.')
    return redirect('treatments:treatment_list')


def services_list_loyalty(request, pk):
    services = get_object_or_404(Service, id=pk, is_active=True)
    treatment_list = Treatment.objects.filter(service=services)
    template_name = 'treatments/treatment_list_loyalty.html'
    context = {'services': services, 'treatment_list': treatment_list}
    return render(request, template_name, context)


def service_loyalty(request):
    services = Service.objects.filter(is_active=True)
    template_name = 'treatments/treatment_list_loyalty.html'
    context = {'services': services}
    return render(request, template_name, context)


