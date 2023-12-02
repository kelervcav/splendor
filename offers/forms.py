from django.forms import ModelForm
from django import forms

from offers.models import Offer, file_size
from treatments.models import Treatment


class OfferForm(ModelForm):
    treatment = forms.ModelChoiceField(
        queryset=Treatment.objects.exclude(is_active=False),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}),
        error_messages={
            'required': 'Please select a service.',
        },
    )

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
        initial=False,
    )

    class Meta:
        model = Offer
        fields = ['title',
                  'treatment',
                  'code',
                  'percentage_discount',
                  'offer_image',
                  'is_offer_active']

