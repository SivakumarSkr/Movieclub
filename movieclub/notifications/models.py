from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
import uuid
from django.utils.translation import ugettext_lazy as _
from django.utils.timesince import timesince


# Create your models here.
class NotificationQuerySet(models.query.QuerySet):

    def get_unread(self):
        return self.filter(unread=True)

    def get_read(self):
        return self.filter(unread=False)

    def mark_all_as_read(self, receiver):
        qu_set = self.get_unread().filter(receiver=receiver)
        qu_set.update(unread=False)

    def get_latest(self, receiver):
        qu_set_unread = self.get_unread().filter(receiver=receiver)[:5]
        qu_set_read = self.get_read().filter(receiver=receiver)[:5]
        return (qu_set_unread + qu_set_read)[:5]


class Notification(models.Model):
    LIKED = 'L'
    COMMENTED = 'C'
    SHARED = 'S'
    ANSWERED = 'A'
    FOLLOWING = 'F'
    POSTED = 'P'
    REPLIED = 'R'

    NOTIFICATION_TYPE = (
        (LIKED, 'liked'),
        (COMMENTED, 'commented'),
        (SHARED, 'shared'),
        (ANSWERED, 'answered'),
        (FOLLOWING, 'following'),
        (POSTED, 'posted'),
        (REPLIED, 'replied'),

    )
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='creator')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver',
                                 blank=False)
    unread = models.BooleanField(default=True)
    slug = models.SlugField(max_length=210, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=1, choices=NOTIFICATION_TYPE)
    subject_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             blank=True, null=True, related_name='subject')
    subject_object_id = models.CharField(max_length=50, blank=True, null=True)
    subject_object = GenericForeignKey('subject_content_type', 'subject_object_id')
    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("-time",)

    def __unicode__(self):
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('{} {} {}'.format(self.uuid_id, self.receiver, self.category),
                                to_lower=True, max_length=200)
        super().save(*args, **kwargs)

    def time_since(self):
        return timesince(self.time, timezone.now())

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
