import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import ugettext_lazy as _

# Create your models here.

User = get_user_model()


class NotificationQuerySet(models.query.QuerySet):

    def mark_all_as_read(self, user_received):
        qu_set = self.get_unread(user_received).filter(receiver=user_received)
        qu_set.update(unread=False)

    def get_latest(self, user_received):
        qu_set_unread = self.get_unread(user_received).filter(receiver=user_received)[:5]
        qu_set_read = self.get_read(user_received).filter(receiver=user_received)[:5]
        return qu_set_unread | qu_set_read


class Notification(models.Model):
    LIKED = 'LK'
    COMMENTED = 'CM'
    SHARED = 'SR'
    ANSWERED = 'AN'
    FOLLOWING = 'FL'
    POSTED = 'PT'
    REPLIED = 'RP'
    SUGGESTION = 'SG'
    JOIN_REQUEST = 'JR'
    REQUEST_APPROVED = 'RA'

    NOTIFICATION_TYPE = (
        (LIKED, 'likes'),
        (COMMENTED, 'commented'),
        (SHARED, 'shared'),
        (ANSWERED, 'answered'),
        (FOLLOWING, 'following'),
        (POSTED, 'posted'),
        (REPLIED, 'replied'),
        (SUGGESTION, 'suggestion'),
        (JOIN_REQUEST, 'group join'),
        (REQUEST_APPROVED, 'request approved'),
    )
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='creator')
    receiver = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notifications', blank=False)
    unread = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=2, choices=NOTIFICATION_TYPE)
    subject_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='subject', )
    subject_object_id = models.CharField(max_length=40)
    subject_object = GenericForeignKey('subject_content_type', 'subject_object_id')
    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("-time",)

    def __unicode__(self):
        pass

    @property
    def time_since(self):
        return timesince(self.time, timezone.now())

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
