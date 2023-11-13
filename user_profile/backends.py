from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(mobile=username) | Q(email=username)
            )

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
