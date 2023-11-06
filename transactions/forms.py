from django import forms
from django.forms import ModelForm
from .models import Transaction
from offers.models import Offer


class TransactionForm(ModelForm):
    reference_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
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
        fields = ['reference_id', 'price_amount', 'offer_code']


