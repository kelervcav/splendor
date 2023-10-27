from django import forms
from django.forms import ModelForm

from .models import Transaction


class AddPointsForm(ModelForm):
    referenced_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    price_amount = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = Transaction
        fields = ['referenced_id', 'price_amount']

