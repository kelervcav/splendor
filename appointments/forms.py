from datetime import datetime

from django import forms
from django.forms import ModelForm, NumberInput
from django.utils import timezone

from treatments.models import Treatment
from user_profile.models import User
from .models import Appointment


class BookingAppointmentForm(forms.ModelForm):
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
        required=True,
        choices=Appointment.TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()

        current_datetime = timezone.now()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')

        if selected_date and selected_date == current_datetime.date() and selected_time:
            current_time = current_datetime.time().strftime('%I:%M %p')
            if selected_time < current_time:
                raise forms.ValidationError("Please select a future time for today.")

        return cleaned_data

    treatment = forms.ModelChoiceField(
        queryset=Treatment.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    class Meta:
        model = Appointment
        fields = [
            'date',
            'time',
            'treatment',
            'is_approved',
        ]
