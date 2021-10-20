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
    national_number = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=[('male', 'Male'), ('female', 'Female')], default='male')
    verified = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='patient')

    has_diabetes = models.BooleanField(default=False)
    has_cancer = models.BooleanField(default=False)
    has_hypertension = models.BooleanField(default=False)
    has_hyperlipidemia = models.BooleanField(default=False)

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


class Medicine(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Result(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='results', null=True, blank=True)
    result_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_results')
    remarks = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    medicines = models.ManyToManyField(Medicine)


class PeriodicMedication(models.Model):
    PERIOD_TYPES = [
        ('once', 'Once'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='periodic_medication', null=True,
                                blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    period = models.CharField(max_length=100, choices=PERIOD_TYPES, default='monthly')

    def is_active(self):
        return self.end_date > timezone.now() if self.end_date else True
