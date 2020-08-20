from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.utils.crypto import get_random_string
import uuid
import random
import string
from django.db.models import F


class Employees(models.Model):
    username = models.OneToOneField(User, on_delete = models.CASCADE)
    employee_code = models.CharField(max_length=500, unique = True, default = uuid.uuid4)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    hourly_rate = models.IntegerField(null = True, blank = True)
    class Meta:
        verbose_name_plural = "Employees"

class Salary(models.Model):
    month = models.IntegerField(null = True, blank = True)
    year = models.IntegerField(null = True, blank = True)
    salary = models.FloatField(null = True, blank = True)
    duration = models.FloatField(null = True, blank = True)
    employee_code = models.ForeignKey(Employees, to_field="employee_code", db_column="employee_code", on_delete = models.CASCADE, null = True, blank = True)
    class Meta:
        verbose_name_plural = "Salary"

class EntryLog(models.Model):
    check_in = models.CharField(max_length=100)
    check_out = models.CharField(max_length=100)
    brea_k = models.CharField(max_length=100)
    duration = models.FloatField(null = True, blank = True)
    date = models.IntegerField(null = True, validators=[
            MaxValueValidator(31),
            MinValueValidator(1)
            ])
    month = models.IntegerField(null = True, validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ])
    year = models.IntegerField(null = True, validators=[
            MinValueValidator(1990)
        ])
    employee_code = models.ForeignKey(Employees, to_field="employee_code", db_column="employee_code", on_delete = models.CASCADE)
    class Meta:
        verbose_name_plural = "Entry Logs"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Employees.objects.get_or_create(username=instance)

post_save.connect(create_user_profile, sender = User)

class ManpowerInvestment(models.Model):
    investment = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    class Meta:
        verbose_name_plural = "ManpowerInvestment"
