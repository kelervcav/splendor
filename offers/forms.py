from django.forms import ModelForm
from django import forms

from offers.models import Offer


class OfferForm(ModelForm):
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

    percentage_discount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    offer_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'}),
    )

    is_offer_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'}),
    )

    class Meta:
        model = Offer
        fields = ['title',
                  'code',
                  'percentage_discount',
                  'offer_image',
                  'is_offer_active']

