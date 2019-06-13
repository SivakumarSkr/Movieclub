import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from django.utils.timezone import now


class CommentQuerySet(models.query.QuerySet):

    @staticmethod
    def get_comments_of_post(post):
        return post.set_comments.all()

    @staticmethod
    def get_user_comments(post, user):
        return post.set_comments.all(user=user)


class Comment(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='comments')
    time = models.DateTimeField(default=now)
    text = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='liked_comments')
    image = models.ImageField(null=True, upload_to='')
    post_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    post_content_object_id = models.CharField(max_length=20)
    post_object = GenericForeignKey('post_content_type', 'post_content_object_id')
    set_comments = GenericRelation('self')
