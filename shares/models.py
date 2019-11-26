import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now


# Create your models here.
class Share(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(default=now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='shares')
    description = models.TextField(null=True, blank=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shares_liked')
    share_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    share_content_object_id = models.CharField(max_length=40, null=True, blank=True)
    sharing_object = GenericForeignKey("share_content_type",
                                       "share_content_object_id")
    set_comments = GenericRelation('comments.Comment')

    def like_the_share(self, user):
        self.liked.add(user)
        self.save()

    def get_comments(self):
        return self.set_comments.all()

    @property
    def get_number_of_likes(self):
        return self.liked.count()
