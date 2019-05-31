from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.

class TopicQuerySet(models.query.QuerySet):
    pass


class Topic(models.Model):
    head = models.CharField(max_length=500)
    time = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic')
    followers = models.ManyToManyField(User, related_name='topic')
