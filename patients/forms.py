from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm, NumberInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AdminPasswordChangeForm
)
from django.utils import timezone

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
        ),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z]*$',
                message='First name must be letters only'),
        ]
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z]*$',
                message='Last name must be letters only'),
        ]
    )
    mobile = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
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

    def clean_date_of_birth(self):
        current_date = timezone.now()
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            check_age = current_date.year - date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day))

            if check_age < 18:
                raise forms.ValidationError("Patient must be 18 and above.")

        return date_of_birth

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

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['gender', 'address']


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

