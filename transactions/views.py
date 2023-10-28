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
#     patient_info = User.objects.all()
#     template_name = 'transaction_list.html'
#     context = {'transactions': transactions, 'patient_info': patient_info}
#     return render(request, template_name, context)


def transaction_create(request, pk):
    form = TransactionForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(id=pk)
        user_profile = UserProfile.objects.get(user=user)
        transaction = form.save(commit=False)
        transaction.user = user
        transaction.save()
        amount = form.cleaned_data['price_amount']
        points_earned = amount / 150
        user_profile.points += points_earned
        user_profile.save()
        messages.success(request, 'Points successfully added.')
        return redirect('patients:patient_info', pk)
    template_name = 'transaction_create.html'
    context = {'form': form}
    return render(request, template_name, context)
