from django.contrib.auth.decorators import login_required, permission_required

from reports.forms import DateRangeForm
from django.shortcuts import render

from reports.utils import most_availed_treatment
from user_profile.decorators import admin_required


# Create your views here.

@login_required
@admin_required
@permission_required('user_profile.view_user', raise_exception=True)
def report(request):
    form = DateRangeForm(request.POST or None)
    if form.is_valid():
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        result = most_availed_treatment(date_from, date_to)
        return render(request, 'generate_report.html', {'form': form, 'result': result})

    return render(request, 'reports.html', {'form': form})


