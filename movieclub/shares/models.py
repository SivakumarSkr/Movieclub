from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from django.conf import settings


# Create your models here.
class Share(models.Model):
    time = models.DateTimeField(default=now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='shares')
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shares_liked')
    share_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    share_content_object_id = models.CharField(max_length=50, null=True, blank=True)
    sharing_object = GenericForeignKey("share_content_type",
                                       "share_content_object_id")
    share_objects = GenericRelation('self')
    set_comments = GenericRelation('comments.Comment')
