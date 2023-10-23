from django import forms
from django.forms import ModelForm, NumberInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AdminPasswordChangeForm
)

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
