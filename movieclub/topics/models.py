from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now


# Create your models here.

class TopicQuerySet(models.query.QuerySet):

    def get_latest_topics(self):
        pass

    def get_trending(self):
        pass

    def get_followed_by_user(self, user):
        pass

    def get_most_followed(self):
        pass

    def get_watched_by_user(self, user):
        pass


class Topic(models.Model):
    head = models.CharField(max_length=500)
    time = models.DateTimeField(default=now, editable=False)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=300, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='topics')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    no_of_watches = models.PositiveIntegerField()

    def follow_the_topic(self, user):
        self.followers.add(user)
        self.save()

    def un_follow_the_topic(self, user):
        self.followers.remove(user)

    def watched(self):
        self.no_of_watches += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.head} {self.time}',
                                to_lower=True, max_length=300)
        super().save(*args, **kwargs)

