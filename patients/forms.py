from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm, NumberInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AdminPasswordChangeForm
)

from user_profile.models import UserProfile

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    mobile = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'mobile'}
        ),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="Phone number must be in format 09123456789"
            )
        ]
    )

    date_of_birth = forms.DateField(
        widget=NumberInput(
            attrs={'type': 'date',
                   'class': 'form-control'},
        )
    )

    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }),
        initial=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'mobile',
            'date_of_birth',
            'is_active',
        )

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.mobile = self.cleaned_data['mobile']
            user.date_of_birth = self.cleaned_data['date_of_birth']

            if commit:
                user.save()
            return user


class CustomRegistration(ModelForm):
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['gender']


class MembershipRenewalForm(ModelForm):
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    mobile = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'mobile'}
        ),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="Phone number must be in format 09123456789"
            )
        ]
    )

    class Meta:
        model = User
        fields = ['email', 'mobile']

