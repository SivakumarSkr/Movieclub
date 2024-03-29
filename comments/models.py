import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
# Create your models here.
from django.utils.timezone import now


class CommentQuerySet(models.query.QuerySet):
    pass


class Comment(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='comments')
    time = models.DateTimeField(default=now, editable=False)
    text = models.TextField()
    edited = models.BooleanField('Edited', default=False, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name='liked_comments')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                      related_name='disliked_comments')
    image = models.ImageField(null=True, blank=True, upload_to='')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=40, blank=True)
    comment_object = GenericForeignKey()
    set_comments = GenericRelation('self')
    objects = CommentQuerySet.as_manager()

    def like(self, user):
        try:
            self.dislikes.remove(user)
        finally:
            self.likes.add(user)
            self.save()

    def dislike(self, user):
        try:
            self.likes.remove(user)
        finally:
            self.dislikes.add(user)
            self.save()

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()

    def get_comments(self):
        return self.set_comments.all()

    class Meta:
        ordering = ('-time',)
