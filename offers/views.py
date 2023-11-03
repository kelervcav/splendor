from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from offers.forms import OfferDiscountForm
from offers.models import Discount


# Create your views here.
def offer_list(request):
    offer_list = Discount.objects.all()
    template_name = 'offer_list.html'
    context = {'offer_list': offer_list}
    return render(request, template_name, context)


def offer_create(request):

    form = OfferDiscountForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Offer created successfully.')
        return redirect('offers:offer_list')
    template_name = 'offer_create.html'
    context = {'form': form}
    return render(request, template_name, context)


def offer_edit(request, pk):
    offer = get_object_or_404(Discount, id=pk)
    form = OfferDiscountForm(request.POST or None, request.FILES or None, instance=offer)
    if form.is_valid():
        form.save()
        messages.success(request, 'Offer has been edited successfully.')
        return redirect('offers:offer_edit', pk)
    template_name = 'offer_edit.html'
    context = {'offer': offer, 'form': form}
    return render(request, template_name, context)


def offer_disable(request, pk):
    offer = get_object_or_404(Discount, id=pk)
    offer.is_discount_active = False
    offer.save()
    messages.success(request, 'Offer has been disabled.')
    return redirect('offers:offer_list')


def offer_list_loyalty(request):
    offers = Discount.objects.filter(is_discount_active=True)
    template_name = 'offer_list_loyalty.html'
    context = {'offers': offers}
    return render(request, template_name, context)
