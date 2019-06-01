from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    contact_no = PhoneNumberField(null=True)
    place = models.CharField(max_length=20, null=True)
    # image = models.ImageField()
