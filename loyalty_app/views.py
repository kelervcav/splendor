from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


# Create your views here.
@login_required
def home(request):
    return render(request,"loyalty/home.html")


def process_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('custom_password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_patient and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home')

            else:
                messages.error(request, "Your username and password didn't match. Please try again.")
                return render(request, 'loyalty/loyalty_login.html')

        else:
            messages.error(request, "Your username and password didn't match. Please try again.")
            return render(request, 'loyalty/loyalty_login.html')

    return render(request, 'loyalty/loyalty_login.html',)


def process_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
