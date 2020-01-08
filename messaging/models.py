import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Message(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid3, primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receive_messages')
    text = models.TextField(max_length=500)
    seen = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='')
    seen_time = models.DateTimeField(null=True, blank=True)
    delivered = models.BooleanField(default=False)
