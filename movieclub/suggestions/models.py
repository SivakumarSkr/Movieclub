import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class SuggestionQuerySet(models.query.QuerySet):

    def get_suggestions_as_sender(self, sender):
        return self.filter(sender=sender)

    def get_suggestions_as_receiver(self, receiver):
        return self.filter(receiver=receiver)


class Suggestion(models.Model):
    # uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='suggest_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                 related_name='suggest_receiver')
    time = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()
    objects = SuggestionQuerySet.as_manager()

    # def get_notification_text(self):
    #     text = '{} suggested a {} for you.'.format(self.sender, self.content_type)
    #     return text
