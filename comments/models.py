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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name='liked_comments')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                      related_name='disliked_comments')
    image = models.ImageField(null=True, blank=True, upload_to='')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=40, blank=True)
    content_object = GenericForeignKey()
    set_comments = GenericRelation('self')
    objects = CommentQuerySet()

    class Meta:
        ordering = ('-time',)

    def like_the_comment(self, user):
        try:
            self.dislikes.remove(user)
        finally:
            self.likes.add(user)
            self.save()

    def dislike_the_comment(self, user):
        try:
            self.likes.remove(user)
        finally:
            self.dislikes.add(user)
            self.save()

    def get_no_likes(self):
        return self.likes.count()

    def get_no_dislikes(self):
        return self.dislikes.count()

    def get_comments(self):
        return self.set_comments

    # def add_comment(self, obj):
    #     self.content_object = obj
    #     self.save()

