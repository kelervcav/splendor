from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model

from user_profile.models import UserProfile

User = get_user_model()


# Create your views here.
@login_required
def home(request):
    return render(request, "loyalty/home.html")


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

