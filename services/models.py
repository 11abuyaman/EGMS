import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    phone = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    national_number = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='patient')

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return "https://pbs.twimg.com/profile_images/740272510420258817/sd2e6kJy_400x400.jpg"


class Department(models.Model):
    name = models.CharField(max_length=120)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    date = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='d_appointments')
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p_appointments', null=True, blank=True)

    def is_this_week(self):
        d = self.date
        now = datetime.datetime.now()
        return (d - timezone.now()).days < 7

    def is_this_month(self):
        d = self.date
        now = datetime.datetime.now()
        return (d - timezone.now()).days < 30

    def appointment_passed(self):
        return self.date < timezone.now()
