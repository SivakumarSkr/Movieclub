from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now


# Create your models here.
class Content(models.Model):
    time = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content')
    contents = models.TextField()
    # content_type_obj = models.ForeignKey(ContentType, on_delete=models.CASCADE)
