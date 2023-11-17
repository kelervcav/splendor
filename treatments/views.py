from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from user_profile.decorators import admin_required
from .forms import ServiceForm, TreatmentForm, AreaForm, TypeForm
from .models import Service, Treatment, TreatmentArea, PriceType
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
@permission_required('treatments.view_treatmentarea', raise_exception=True)
def area_list(request):
    treatment_area_list = TreatmentArea.objects.all().order_by('-created_at')
    template_name = 'treatments/area_list.html'
    context = {'treatment_area_list': treatment_area_list}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.add_treatmentarea', raise_exception=True)
def area_create(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Treatment area created successfully.')
        return redirect('treatments:area_list')
    template_name = 'treatments/area_create.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.change_treatmentarea', raise_exception=True)
def area_edit(request, pk):
    treatment_area = get_object_or_404(TreatmentArea, id=pk)
    form = AreaForm(request.POST or None, instance=treatment_area)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Treatment area updated successfully.')
        return redirect('treatments:area_edit', pk)
    template_name = 'treatments/area_edit.html'
    context = {'area': treatment_area, 'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.disable_treatmentarea', raise_exception=True)
def area_disable(request, pk):
    treatment_area = get_object_or_404(TreatmentArea, id=pk)
    treatment_area.is_active = False
    treatment_area.save()
    messages.success(request, 'Treatment area has been marked as inactive.')
    return redirect('treatments:area_list')


@login_required
@admin_required
@permission_required('treatments.view_pricetype', raise_exception=True)
def price_type_list(request):
    pricing_type_list = PriceType.objects.all().order_by('-created_at')
    template_name = 'treatments/pricetype_list.html'
    context = {'pricing_type_list': pricing_type_list}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.add_pricetype', raise_exception=True)
def price_type_create(request):
    form = TypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Price type created successfully.')
        return redirect('treatments:price_type_list')
    template_name = 'treatments/pricetype_create.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.change_pricetype', raise_exception=True)
def price_type_edit(request, pk):
    price_type = get_object_or_404(PriceType, id=pk)
    form = TypeForm(request.POST or None, instance=price_type)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Price type updated successfully.')
        return redirect('treatments:price_type_edit', pk)
    template_name = 'treatments/pricetype_edit.html'
    context = {'price_type': price_type, 'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('treatments.disable_pricetype', raise_exception=True)
def price_type_disable(request, pk):
    price_type = get_object_or_404(PriceType, id=pk)
    price_type.is_active = False
    price_type.save()
    messages.success(request,
                     'Price type has been marked as inactive.')
    return redirect('treatments:price_type_list')


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
