from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm

from .models import Service, Treatment, TreatmentArea, PriceType


class ServiceForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Service name must be letters only'),
        ],
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'}))

    class Meta:
        model = Service
        fields = ['name', 'description']


class TreatmentForm(ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.exclude(status='Deleted'),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}),
        error_messages={
            'required': 'Please select a service.',
        },
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Treatment name must be letters only'),
        ],
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'}))

    area = forms.ModelChoiceField(
        queryset=TreatmentArea.objects.exclude(status='Deleted'),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    type = forms.ModelChoiceField(
        queryset=PriceType.objects.exclude(status='Deleted'),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    price = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = Treatment
        fields = [
            'service',
            'name',
            'description',
            'area',
            'type',
            'price',
        ]


class AreaForm(ModelForm):
    area = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Treatment area must be letters only'),
        ],
    )

    class Meta:
        model = TreatmentArea
        fields = ['area']


class TypeForm(ModelForm):
    type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Price type must be letters only'),
        ],
    )

    class Meta:
        model = PriceType
        fields = ['type']

