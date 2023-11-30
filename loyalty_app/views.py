from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model
from treatments.models import Service
from offers.models import Offer
from transactions.models import Transaction
from user_profile.models import UserProfile

User = get_user_model()


# Create your views here.
@login_required
def home(request):
    user = request.user
    transaction_list = Transaction.objects.filter(user=user).order_by('-date_added')[:5]
    offers = Offer.objects.filter(is_offer_active=True)
    services = Service.objects.filter(is_active=True)
    template_name = 'loyalty/home.html'
    context = {'transaction_list': transaction_list, 'users': user, 'offers': offers, 'services': services}
    return render(request, template_name, context)


def process_login(request):
    if request.method == 'POST':
        username = request.POST.get('mobile')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        date_now = datetime.now()

        if user is not None:
            if user.is_patient:
                if date_now > user.userprofile.account_expiry:
                    messages.error(request, "Your account is already expired. Please renew your account.")
                    return render(request, 'loyalty/loyalty_login.html')

                else:
                    login(request, user)
                    return HttpResponseRedirect('/home')

            else:
                messages.error(request, "Your username and password didn't match. Please try again.")
                return render(request, 'loyalty/loyalty_login.html')

        else:
            messages.error(request, "Your username and password didn't match. Please try again.")
            return render(request, 'loyalty/loyalty_login.html')

    return render(request, 'loyalty/loyalty_login.html')

