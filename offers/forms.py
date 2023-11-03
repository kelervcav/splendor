from django.forms import ModelForm
from django import forms

from offers.models import Discount


class OfferDiscountForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    start_date = forms.DateField(
        widget=forms.NumberInput(
            attrs={'type': 'date',
                   'class': 'form-control'}),
    )

    end_date = forms.DateField(
        widget=forms.NumberInput(
            attrs={'type': 'date',
                   'class': 'form-control'}),
    )

    offer_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'}),
    )

    is_discount_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'}),
    )

    class Meta:
        model = Discount
        fields = ['title',
                  'code',
                  'start_date',
                  'end_date',
                  'offer_image',
                  'is_discount_active']
