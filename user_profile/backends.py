from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(mobile=username, is_patient=True)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username, is_patient=False)
            except User.DoesNotExist:
                return None

        if user.is_patient and user.check_password(password):
            # Patients can only log in using mobile number
            return user
        elif not user.is_patient and user.check_password(password):
            # Therapists can only log in using email
            return user
        return None
