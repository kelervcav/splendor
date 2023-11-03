from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

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
    form = TransactionForm(request.POST or None)
    if form.is_valid():
        user_profile = UserProfile.objects.get(user=user)
        transaction = form.save(commit=False)
        transaction.user = user
        amount = form.cleaned_data['price_amount']
        transaction.points = amount / 150
        transaction.save()
        user_profile.total_points += transaction.points
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


