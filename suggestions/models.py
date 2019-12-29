import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


# Create your models here.
class SuggestionQuerySet(models.query.QuerySet):

    def get_suggestions_as_sender(self, sender):
        return self.filter(sender=sender)

    def get_suggestions_as_receiver(self, receiver):
        return self.filter(receiver=receiver)


class Suggestion(models.Model):
    THANKS = 'T'
    ALL_READY_WATCHED = 'A'
    BAD_SUGGEST = 'C'
    choices = (
        (THANKS, 'Thanks'),
        (ALL_READY_WATCHED, "You are late."),
        (BAD_SUGGEST, 'Bad choice.')
    )
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='suggest_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                 related_name='suggest_receiver')
    time = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.CharField(max_length=40, null=True, blank=True)
    content_object = GenericForeignKey()
    share_object = GenericRelation('shares.Share')
    response = models.CharField(max_length=1, choices=choices, null=True)
    objects = SuggestionQuerySet.as_manager()
    notification = GenericRelation('notifications.Notification')

    def respond(self, response):
        self.response = response
        self.save()
