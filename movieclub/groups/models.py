from django.db import models


# Create your models here.
class Group(models.Model):
    name = models.CharField('Name', max_length=30)

