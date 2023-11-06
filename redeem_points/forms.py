from django.forms import ModelForm
from django import forms
from redeem_points.models import RedeemPoints


class RedeemPointsForm(ModelForm):
    redeemed_points = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = RedeemPoints
        fields = ['redeemed_points']
