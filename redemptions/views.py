from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect

from redemptions.forms import RedemptionForm
from redemptions.models import Redemption
from user_profile.models import UserProfile

User = get_user_model()


# Create your views here.
def redeem_points(request, pk):
    user = User.objects.get(id=pk)
    user_profile = UserProfile.objects.get(user=user)
    redemption = Redemption.objects.filter(user=user).first()
    form = RedemptionForm(request.POST or None, instance=user, initial={'redemption': redemption})
    if form.is_valid():
        redeem = form.save(commit=False)
        redeem.user = user
        redeem.redeem_points = form.cleaned_data['redeemed_points']
        user_profile.total_points -= redeem.redeem_points
        user_profile.save()
        if redemption is not None:
            redemption.redeemed_points += redeem.redeem_points
        else:
            redemption = Redemption(user=user, redeemed_points=redeem.redeem_points)
        redeem.save()
        redemption.save()
        messages.success(request, 'Points redeemed successfully.')
        return redirect('redemptions:redeemed_points_list', pk)
    template_name = 'redeem_points.html'
    context = {'form': form, 'users': user}
    return render(request, template_name, context)


def redeemed_points_list(request, pk):
    redeemed_list = Redemption.objects.filter(user=pk).order_by('-date_redeemed')
    template_name = 'redeemed_points_list.html'
    context = {'redeemed_list': redeemed_list}
    return render(request, template_name, context)
