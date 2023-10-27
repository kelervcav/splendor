from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddPointsForm
from .models import Transaction
from user_profile.models import UserProfile, User

User = get_user_model()


# Create your views here.
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date_added')
    template_name = 'transaction_list.html'
    context = {'transactions': transactions}
    return render(request, template_name, context)


def transaction_create(request, pk):
    form = AddPointsForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(id=pk)
        transaction = form.save(commit=False)
        transaction.user = user
        transaction.save()
        messages.success(request, 'Points successfully added.')
        return redirect('patients:patient_info', pk)
    template_name = 'transaction_create.html'
    context = {'form': form}
    return render(request, template_name, context)
