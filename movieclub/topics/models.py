import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from taggit.managers import TaggableManager


# Create your models here.

class TopicQuerySet(models.query.QuerySet):

    def get_latest_topics(self):
        return self.order_by('-time')

    def get_trending(self):
        return self.order_by('no_of_watches')

    def get_most_followed(self):
        pass


class Topic(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    head = models.CharField(max_length=500)
    time = models.DateTimeField(default=now, editable=False)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=300, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='topics')
    tags = TaggableManager()
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='topics_followed', blank=True)
    no_of_watches = models.PositiveIntegerField(default=0)
    suggestion = GenericRelation('suggestions.Suggestion')
    objects = TopicQuerySet.as_manager()

    class Meta:
        ordering = ("-time",)
        get_latest_by = 'time'

    def follow_the_topic(self, user):
        self.followers.add(user)
        self.save()

    def un_follow_the_topic(self, user):
        self.followers.remove(user)
        self.save()

    def watched(self):
        self.no_of_watches += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.head} {self.time}", )
        super().save(*args, **kwargs)
