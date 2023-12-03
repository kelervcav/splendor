from transactions.models import Transaction
from user_profile.models import User
from django.db.models import Count, Sum, F
from django.shortcuts import get_object_or_404

from appointments.models import Appointment
from treatments.models import Treatment


def most_availed_treatment(date_from, date_to):
    result = (
        Appointment.objects
        .filter(date__range=[date_from, date_to], is_approved=True)
        .values('treatment')
        .annotate(count=Count('treatment'))
    )
    for treatment in result:
        treatment_id = treatment.get('treatment')
        treatment_instance = get_object_or_404(Treatment, pk=treatment_id)
        treatment['treatment_name'] = treatment_instance.name

    return result


def get_patients(date_from, date_to):
    patients = (User.objects
                .filter(is_patient=True, created_at__range=[date_from, date_to])
                .order_by('created_at')
                .select_related('userprofile'))

    return patients


def get_treatments(date_from, date_to):
    treatments = (Treatment.objects
                  .filter(created_at__range=[date_from, date_to])
                  .order_by('created_at'))

    return treatments


def get_canceled_appointment(date_from, date_to):
    canceled_appointment = (Appointment.objects
                            .filter(date__range=[date_from, date_to], is_cancel=True)
                            .order_by('created_at'))

    return canceled_appointment


def total_sales_report(date_from, date_to):
    total_sales = Transaction.objects.filter(date_added__range=[date_from, date_to]).aggregate(
        total_sales=Sum(F('price_amount') + F('discounted_amount'))
        )['total_sales']
    total_sales = total_sales or 0

    return total_sales
