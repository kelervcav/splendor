from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not mobile:
            raise ValueError('The Phone Number field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, mobile, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'first_name', 'last_name']

    def set_custom_password(self):
        surname = self.last_name.lower()
        underscore = '_'
        birthdate = self.date_of_birth.strftime('%Y%m%d')
        custom_password = f"{surname}{underscore}{birthdate}"
        self.set_password(custom_password)
        self.save()

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'user'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('', '---------'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, )
    notes = models.TextField(null=True, blank=True)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    account_expiry = models.DateTimeField(default=datetime.now() + timedelta(days=365))

    # Add any additional fields you need for your user profile

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'user_profile'
