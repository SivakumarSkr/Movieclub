import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import F
from django.utils.text import slugify
from taggit.managers import TaggableManager


# Create your models here.

class TopicQuerySet(models.query.QuerySet):

    def get_latest_topics(self):
        return self.order_by('-time')

    def get_trending(self):
        return self.order_by('-no_of_watches')


class Topic(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    head = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=300, null=False, blank=True)
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

    def follow(self, user):
        if not self.check_the_follow(user):
            self.followers.add(user)
            self.save()
            return True
        else:
            return False

    def check_the_follow(self, user):
        return self.followers.all().filter(pk=user.pk).exists()

    def un_follow(self, user):
        if self.check_the_follow(user):
            self.followers.remove(user)
            self.save()
            return True
        else:
            return False

    def watched(self):
        self.no_of_watches = F('no_of_watches') + 1
        self.save()

    @property
    def followers_count(self):
        return self.followers.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.head}", )
        super().save(*args, **kwargs)

    @property
    def answer_count(self):
        answer_count = self.answer_set.count()
        return answer_count
