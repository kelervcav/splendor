import time
from datetime import datetime

from django import forms
from django.forms import ModelForm, NumberInput
from django.utils import timezone

from treatments.models import Treatment
from user_profile.models import User
from .models import Appointment


class BookingAppointmentForm(forms.ModelForm):
    treatment = forms.ModelChoiceField(
        queryset=Treatment.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'}))

    date = forms.DateField(
        widget=NumberInput(
            attrs={'type': 'date',
                   'class': 'form-control'}),
        error_messages={
            'invalid_date': 'Please select future date.',
            'time_in_past': 'Selected time has already passed.',
        }
    )

    time = forms.ChoiceField(
        required=True,
        choices=Appointment.TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': 'This field is required.',
            'time_in_past': 'Selected time has already passed.',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_time = cleaned_data.get('time')
        selected_date = self.cleaned_data.get('date')

        if selected_date:
            current_date = timezone.now().date()
            if selected_date < current_date:
                 self.add_error('date', self.fields['date'].error_messages['invalid_date'])

            if selected_time != '--:-- --':
                selected_datetime = datetime.combine(selected_date, datetime.strptime(selected_time, '%H:%M:%S').time())
                current_datetime = timezone.now()
                if selected_datetime <= current_datetime:
                     self.add_error('time', self.fields['time'].error_messages['time_in_past'])

        return cleaned_data

    class Meta:
        model = Appointment
        fields = [
            'date',
            'time',
            'treatment',
            'is_approved',
        ]
