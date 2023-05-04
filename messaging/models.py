import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


# Create your models here.
class Chat(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=40)
    participants = models.ManyToManyField(User, related_name="chats", limit_choices_to=2)
    time_started = models.DateTimeField(auto_now_add=True)

    def get_unread_messages(self):
        return self.get_all_messages().filter(seen=False)

    def get_all_messages(self):
        return self.chat_messages.all()

    @property
    def last_active_time(self):
        # time at which last message sent in this chat
        return self.get_all_messages().latest().time

    def last_message(self):
        return self.chat_messages.latest()

    @property
    def number_of_unread_message(self):
        return self.get_unread_messages().count()

    def is_participant(self, user):
        return self.participants.filter(pk=user.pk).exist()


class Message(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid3, primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receive_messages')
    text = models.TextField(max_length=500)
    chat = models.ForeignKey(Chat, related_name="chat_messages", on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='')
    seen_time = models.DateTimeField(null=True, blank=True)
    delivered = models.BooleanField(default=False)
    parent = models.ForeignKey('messaging.Message', on_delete=models.CASCADE, null=True, blank=True)

    def set_seen(self):
        if not self.seen:
            self.seen = True
            self.seen_time = timezone.now()
            self.save()

    def set_delivered(self):
        if not self.delivered:
            self.delivered = True
            self.save()

    class Meta:
        ordering = ['-time']
        get_latest_by = ['-time']
