from django import forms
from django.forms import ModelForm

from .models import Transaction
from treatments.models import Treatment


class AddPointsForm(ModelForm):
    treatment = forms.ModelChoiceField(
        queryset=Treatment.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'})
    )

    price_amount = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = Transaction
        fields = ['treatment', 'price_amount']
