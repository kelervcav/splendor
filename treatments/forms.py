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
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
            }))

    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }),
        initial=True

    )

    class Meta:
        model = Service
        fields = ['name', 'description', 'is_active']


class TreatmentForm(ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.exclude(is_active=False),
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
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
            }))

    area = forms.ModelChoiceField(
        queryset=TreatmentArea.objects.exclude(is_active=False),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    type = forms.ModelChoiceField(
        queryset=PriceType.objects.exclude(is_active=False),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }),
        initial=True

    )

    class Meta:
        model = Treatment
        fields = [
            'service',
            'name',
            'description',
            'area',
            'type',
            'is_active'
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

    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }),
        initial=True

    )

    class Meta:
        model = TreatmentArea
        fields = ['area', 'is_active']


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

    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }),
        initial=True
    )

    class Meta:
        model = PriceType
        fields = ['type', 'is_active']

