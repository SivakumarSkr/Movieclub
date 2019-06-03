from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from topics.models import Topic
from movies.models import Movie


# Create your models here.
class Content(models.Model):
    time = models.DateTimeField(default=now, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contents = models.TextField()
    watched = models.PositiveIntegerField(default=0)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="%(class)s_liked")
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name="%(class)s_disliked")

    class Meta:
        abstract = True

    def content_watched(self):
        self.watched += 1
        self.save()

    def like_the_content(self, user):
        try:
            self.disliked.remove(user)
        finally:
            self.liked.add(user)
            self.save()

    def dislike_the_content(self, user):
        try:
            self.liked.remove(user)
        finally:
            self.disliked.add(user)
            self.save()

    def get_likes(self):
        return self.liked.count()

    def get_dislike(self):
        return self.disliked.count()


class Blog(Content):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-time",)


class Review(Content):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-time",)
