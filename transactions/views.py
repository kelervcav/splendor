from _decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from offers.models import Offer
from user_profile.models import UserProfile
from .forms import TransactionForm
from .models import Transaction

User = get_user_model()


# Create your views here.
# def transaction_list(request):
#     transactions = Transaction.objects.all().order_by('-date_added')
#     template_name = 'transaction_list.html'
#     context = {'transactions': transactions}
#     return render(request, template_name, context)


def transaction_create(request, pk):
    user = User.objects.get(id=pk)
    user_profile = UserProfile.objects.get(user=user)
    offers = Offer.objects.all()
    form = TransactionForm(request.POST or None)

    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = user
        if transaction.offer_code:
            if transaction.is_code_used:
                for offer in offers:
                    if transaction.offer_code == offer.code:
                        discount = offer.percentage_discount
                        percent_discount = Decimal(discount / 100)  # convert discount into percentage
                        amount = form.cleaned_data['price_amount']
                        new_amount = amount - (percent_discount * amount)  # new amount after using discount in percent
                        transaction.points = new_amount / 150  # points on each transaction
                        transaction.is_code_used = True
                        transaction.save()
                        user_profile.total_points += transaction.points  # total points on each transaction
                        user_profile.save()
                    else:
                        messages.error(request, 'Invalid offer code.')
                        return redirect('transactions:transaction_create', pk)
            else:
                messages.error(request, 'Offer code was already used.')
                return redirect('transactions:transaction_create', pk)
        else:
            amount = form.cleaned_data['price_amount']
            transaction.points = amount / 150  # points each transaction
            transaction.save()
            user_profile.total_points += transaction.points  # total points on each transaction
            user_profile.save()

        messages.success(request, 'Points added successfully.')
        return redirect('patients:patient_info', pk)
    template_name = 'transaction_create.html'
    context = {'form': form, 'users': user}
    return render(request, template_name, context)


def transaction_history(request):
    user = User.objects.all()
    transaction_list = Transaction.objects.all()
    template_name = 'transaction_history_list.html'
    context = {'transaction_list': transaction_list, 'users': user}
    return render(request, template_name, context)
