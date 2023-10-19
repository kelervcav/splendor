from datetime import datetime

from django import forms
from django.forms import ModelForm, NumberInput
from django.utils import timezone

from treatments.models import Treatment
from user_profile.models import User
from appointments.models import Appointment


class BookingAppointmentForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_patient=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    date = forms.DateField(
        widget=NumberInput(
            attrs={'type': 'date',
                   'class': 'form-control'},
        )
    )

    def clean_date(self):
        current_date = timezone.now()
        date = self.cleaned_data['date']

        if date < current_date.date():
            raise forms.ValidationError("Please select a future date.")
        return date

    time = forms.ChoiceField(
        choices=Appointment.TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    treatment = forms.ModelChoiceField(
        queryset=Treatment.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    class Meta:
        model = Appointment
        fields = [
            'user',
            'date',
            'time',
            'treatment',
        ]