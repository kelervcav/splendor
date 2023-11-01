from django.forms import ModelForm
from django import forms
from redemptions.models import Redemption


class RedemptionForm(ModelForm):
    redeemed_points = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = Redemption
        fields = ['redeemed_points']
