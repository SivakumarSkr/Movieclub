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

    class Meta:
        abstract = True


class Blog(Content):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-time",)


class Review(Content):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-time",)
