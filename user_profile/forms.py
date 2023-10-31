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

#
# class LoginForm(AuthenticationForm):
#
#     username = forms.CharField(  # This is always 'username'
#         max_length=100,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'name': 'email',
#                 'placeholder': 'Email'}
#         )
#     )
#     password = forms.CharField(
#         max_length=100,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'name': 'password',
#                 'placeholder': 'Password'}
#         )
#     )


class ProfileCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(
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
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'mobile',
            'is_active',
        )

    def save(self, commit=True):
        user = super(ProfileCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobile = self.cleaned_data['mobile']

        if commit:
            user.save()
            user.groups.clear()
            user.groups.add(self.cleaned_data['group'])

        return user


class EditProfileForm(UserChangeForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'})
    )
    mobile = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                 'class': 'form-control',
                 'name': 'mobile'})
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
            'password',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'is_active',
        )


class UserProfileEdit(ModelForm):
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

    class Meta:
        model = User
        fields = (
            'mobile',
        )


class AdminEditPasswordForm(AdminPasswordChangeForm):
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control'}))
    password2 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control'}))


