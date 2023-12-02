from django import forms
from django.forms import ModelForm

from redeem_points.models import RedeemPoints
from treatments.models import Treatment
from .models import Transaction
from offers.models import Offer


class TransactionForm(ModelForm):
    treatment = forms.ModelChoiceField(
        queryset=Treatment.objects.exclude(is_active=False),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}),
        error_messages={
            'required': 'Please select a service.',
        },
    )

    price_amount = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    offer_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    def clean_offer_code(self):
        offer_code = self.cleaned_data['offer_code']
        if offer_code:
            try:
                Offer.objects.get(code=offer_code)

            except Offer.DoesNotExist:
                raise forms.ValidationError('Invalid offer code.')
        return offer_code

    class Meta:
        model = Transaction
        fields = ['treatment', 'price_amount', 'offer_code']


class RedeemPointsForm(ModelForm):
    redeemed_points = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = RedeemPoints
        fields = ['redeemed_points']

