from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

from offers.forms import OfferForm
from offers.models import Offer
from treatments.models import Service
from user_profile.decorators import admin_required


# Create your views here.
@login_required
@admin_required
@permission_required('offers.view_offer', raise_exception=True)
def offer_list(request):
    offer_list = Offer.objects.all()
    template_name = 'offer_list.html'
    context = {'offer_list': offer_list}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('offers.add_offer', raise_exception=True)
def offer_create(request):
    form = OfferForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Offer created successfully.')
        return redirect('offers:offer_list')
    template_name = 'offer_create.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('offers.change_offer', raise_exception=True)
def offer_edit(request, pk):
    offer = get_object_or_404(Offer, id=pk)
    form = OfferForm(request.POST or None, request.FILES or None, instance=offer)
    if form.is_valid():
        form.save()
        messages.success(request, 'Offer has been edited successfully.')
        return redirect('offers:offer_edit', pk)
    template_name = 'offer_edit.html'
    context = {'offer': offer, 'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('offers.disable_offer', raise_exception=True)
def offer_disable(request, pk):
    offer = get_object_or_404(Offer, id=pk)
    offer.is_offer_active = False
    offer.save()
    messages.success(request, 'Offer has been disabled.')
    return redirect('offers:offer_list')


# For patient
def offer_list_loyalty(request):
    offers = Offer.objects.filter(is_offer_active=True)
    services = Service.objects.filter(is_active=True)
    date_now = datetime.now()
    template_name = 'offer_list_loyalty.html'
    context = {'offers': offers, 'date_now': date_now, 'services': services}
    return render(request, template_name, context)



