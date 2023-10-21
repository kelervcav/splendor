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


class LoginForm(AuthenticationForm):

    username = forms.CharField(  # This is always 'username'
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'email',
                'placeholder': 'Email'}
        )
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password',
                'placeholder': 'Password'}
        )
    )


class AdminGroupForm(ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
    )

    class Meta:
        model = Group
        fields = '__all__'


class ProfileCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(
        required=False,
        queryset=Group.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
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
                regex=r'^[a-zA-Z\s]*$',
                message='Firstname must be letters only'),
        ],
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Lastname must be letters only'),
        ],
    )
    mobile = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'mobile'}
        ),
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
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
            })
    )

    class Meta:
        model = User
        fields = (
            'group',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'mobile',
            'date_of_birth',
            'is_patient',
            'is_active',
        )

    def save(self, commit=True):
        user = super(ProfileCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobile = self.cleaned_data['mobile']
        user.date_of_birth = self.cleaned_data['date_of_birth']

        if commit:
            user.save()
            user.groups.clear()
            user.groups.set(self.cleaned_data['group'])
            return user
