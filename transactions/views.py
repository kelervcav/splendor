from _decimal import Decimal
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from offers.models import Offer
from redeem_points.models import RedeemPoints
from user_profile.decorators import admin_required
from user_profile.models import UserProfile
from .forms import TransactionForm, RedeemPointsForm
from .models import Transaction

User = get_user_model()


@login_required
@admin_required
@permission_required('transactions.add_transaction', raise_exception=True)
def transaction_create(request, pk):
    user = User.objects.get(id=pk)

    user_profile = UserProfile.objects.get(user=user)

    offers = Offer.objects.all()
    transaction_form = TransactionForm(request.POST or None)
    redeem_form = RedeemPointsForm(request.POST or None)

    if transaction_form.is_valid() and redeem_form.is_valid():
        transaction = transaction_form.save(commit=False)
        transaction.user = user
        redeem = redeem_form.save(commit=False)
        redeem.user = user

        if transaction.offer_code:
            for offer in offers:
                if transaction.offer_code.upper() == offer.code:
                    if Transaction.objects.filter(user=user, offer_code=transaction.offer_code).exists():
                        messages.error(request, 'Code was already used.')
                        return redirect('transactions:transaction_create', pk)
                    else:
                        if redeem.redeemed_points:
                            points = redeem_form.cleaned_data['redeemed_points']
                            redeem.redeemed_points = points
                            transaction.save()
                            redeem.transaction = transaction
                            redeem.save()
                            percent_discount = Decimal(offer.percentage_discount / 100)  # convert discount into percentage
                            new_amount = transaction.price_amount - (percent_discount * transaction.price_amount)  # new amount after using offer code
                            if user_profile.total_points >= points:
                                user_profile.total_points -= points
                                user_profile.save()
                                new_updated_amount = new_amount - points  # new updated amount after redeeming points
                                transaction.discounted_amount = new_updated_amount
                                transaction.points = new_updated_amount / 150  # earned points on transaction
                                transaction.offer_code = transaction_form.cleaned_data['offer_code'].upper()
                                transaction.save()
                                user_profile.total_points += transaction.points  # total points on each transaction
                                user_profile.save()
                            else:
                                messages.error(request, 'Insufficient amount of points.')
                                return redirect('transactions:transaction_create', pk)
                        else:
                            percent_discount = Decimal(offer.percentage_discount / 100)
                            new_amount = transaction.price_amount - (percent_discount * transaction.price_amount)  # new amount after using discount in percent
                            transaction.discounted_amount = new_amount
                            transaction.points = new_amount / 150  # points on each transaction
                            transaction.offer_code = transaction_form.cleaned_data['offer_code'].upper()
                            transaction.save()
                            user_profile.total_points += transaction.points  # total points on each transaction
                            user_profile.save()

        else:
            if redeem.redeemed_points:  # check if not empty
                points = redeem_form.cleaned_data['redeemed_points']
                redeem.redeemed_points = points
                transaction.save()
                redeem.transaction = transaction
                redeem.save()
                if user_profile.total_points >= points:
                    user_profile.total_points -= points
                    new_amount = transaction.price_amount - points  # calculate new amount after deducting redeemed points
                    transaction.discounted_amount = new_amount
                    transaction.points = new_amount / 150  # calculate points based on the discounted amount
                    transaction.save()
                    user_profile.total_points += transaction.points   # update total points
                    user_profile.save()
                else:
                    messages.error(request, 'Insufficient amount of points.')
                    return redirect('transactions:transaction_create', pk)
            else:
                transaction.points = transaction.price_amount / 150  # points each transaction
                transaction.save()
                user_profile.total_points += transaction.points  # total points on each transaction
                user_profile.save()

        messages.success(request, 'Points added successfully.')
        return redirect('patients:patient_info', pk)

    template_name = 'transaction_create.html'
    context = {'form': transaction_form, 'users': user, 'redeem_form': redeem_form}
    return render(request, template_name, context)


# Patients UI
def transaction_history(request):
    user = request.user
    transaction_list = Transaction.objects.filter(user=user).order_by('-date_added')
    template_name = 'transaction_history_list.html'
    context = {'transaction_list': transaction_list, 'users': user}
    return render(request, template_name, context)
