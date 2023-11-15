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

    def clean_time(self):
        current_date_time = timezone.now()

        selected_time = self.cleaned_data['time']
        selected_date = self.cleaned_data['date']

        selected_date_time = datetime.combine(selected_date, selected_time)

        if selected_date_time <= current_date_time:
            raise forms.ValidationError("Selected time has already passed.")
        return selected_time

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
