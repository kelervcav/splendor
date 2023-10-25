from django.contrib import messages
from django.shortcuts import render, redirect

from transactions.forms import AddPointsForm
from transactions.models import Transaction


# Create your views here.
def view_points(request):
    points = Transaction.objects.all().order_by('-date_added')
    template_name = 'treatments/service_list.html'
    context = {'points': points}
    return render(request, template_name, context)


def add_points(request):
    form = AddPointsForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Points successfully added.')
        return redirect('')
    template_name = ''
    context = {'form': form}
    return render(request, template_name, context)
