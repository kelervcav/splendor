from _decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from offers.models import Offer
from redeem_points.models import RedeemPoints
from user_profile.decorators import admin_required
from user_profile.models import UserProfile
from .forms import TransactionForm
from .models import Transaction

User = get_user_model()


@login_required
@admin_required
@permission_required('transactions.add_transaction', raise_exception=True)
def transaction_create(request, pk):
    user = User.objects.get(id=pk)
    user_profile = UserProfile.objects.get(user=user)
    offers = Offer.objects.all()
    form = TransactionForm(request.POST or None)

    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = user
        if transaction.offer_code:
            for offer in offers:
                if transaction.offer_code.upper() == offer.code:
                    if Transaction.objects.filter(user=user, offer_code=transaction.offer_code).exists():
                        messages.error(request, 'Code was already used.')
                        return redirect('transactions:transaction_create', pk)
                    else:
                        discount = offer.percentage_discount
                        percent_discount = Decimal(discount / 100)  # convert discount into percentage
                        amount = form.cleaned_data['price_amount']
                        new_amount = amount - (percent_discount * amount)  # new amount after using discount in percent
                        transaction.discounted_amount = new_amount
                        transaction.points = new_amount / 150  # points on each transaction
                        transaction.offer_code = form.cleaned_data['offer_code'].upper()
                        transaction.save()
                        user_profile.total_points += transaction.points  # total points on each transaction
                        user_profile.save()
        else:
            amount = form.cleaned_data['price_amount']
            transaction.points = amount / 150  # points each transaction
            transaction.save()
            user_profile.total_points += transaction.points  # total points on each transaction
            user_profile.save()

        messages.success(request, 'Points added successfully.')
        return redirect('transactions:transaction_create', pk)
    template_name = 'transaction_create.html'
    context = {'form': form, 'users': user}
    return render(request, template_name, context)


# Patients UI
def transaction_history(request):
    user = request.user
    transaction_list = Transaction.objects.filter(user=user).order_by('-date_added')
    template_name = 'transaction_history_list.html'
    context = {'transaction_list': transaction_list, 'users': user}
    return render(request, template_name, context)
