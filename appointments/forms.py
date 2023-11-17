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
                   'class': 'form-control'},
        )
    )

    def clean_date(self):
        current_date = timezone.now()
        date = self.cleaned_data.get('date')
        if date and date < current_date.date():
            raise forms.ValidationError("Please select a future date.")
        return date

    time = forms.ChoiceField(
        required=True,
        choices=Appointment.TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': 'This field is required.',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')

        if selected_date and selected_time:
            current_date_time = timezone.now()
            if selected_time and selected_time != '--:-- --':
                selected_date_time = datetime.combine(selected_date,
                                                      datetime.strptime(selected_time, '%H:%M:%S').time())

                if selected_date_time <= current_date_time:
                    raise forms.ValidationError("Selected date and time must be in the future.")

        return cleaned_data

    class Meta:
        model = Appointment
        fields = [
            'date',
            'time',
            'treatment',
            'is_approved',
        ]
