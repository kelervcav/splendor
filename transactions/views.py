from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddPointsForm
from .models import Transaction
from user_profile.models import UserProfile, User

User = get_user_model()


# Create your views here.
def view_points(request):
    points = Transaction.objects.all().order_by('-date_added')
    template_name = 'treatments/service_list.html'
    context = {'points': points}
    return render(request, template_name, context)


def create_transaction(request, pk):
    form = AddPointsForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(id=pk)
        transaction = form.save(commit=False)
        transaction.user = user
        transaction.save()
        messages.success(request, 'Points successfully added.')
        return redirect('patients:patient_list')

    template_name = 'add_transaction.html'
    context = {'form': form}
    return render(request, template_name, context)
