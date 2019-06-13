from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from topics.models import Topic
from movies.models import Movie
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.
class ContentQuerySet(models.query.QuerySet):

    def get_published(self):
        return self.filter(status='P')

    def get_drafts(self):
        return self.filter(status='D')


class Content(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )
    time = models.DateTimeField(default=now, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    watched = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS, default='D')
    tags = TaggableManager()
    contents = MarkdownxField(null=True)

    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="%(class)s_liked")
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name="%(class)s_disliked")
    suggestion = GenericRelation('suggestions.Suggestion')
    objects = ContentQuerySet.as_manager()
    share_object = GenericRelation('shares.Share')
    image = models.ImageField(upload_to='contents/%(class)/%Y/%m/%d', null=True)
    set_comments = GenericRelation('comments.Comment')

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

    def get_markdown(self):
        return markdownify(self.content)


class Answer(Content):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ("-time",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(slugify(self.topic))

        super().save(*args, **kwargs)


class Review(Content):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    spoiler_alert = models.BooleanField(default=False)

    class Meta:
        ordering = ("-time",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("{}'s review on {} {}".format(
                self.user.name, self.movie.name, self.movie.released_year))
        super().save(*args, **kwargs)


class Blog(Content):
    heading = models.CharField(max_length=300)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.heading)
        super().save(*args, **kwargs)


class Status(models.Model):
    WATCHING = 'W'
    FEELING = 'F'
    ACTION = (
        (WATCHING, 'Watching'),
        (FEELING, 'Feeling'),

    )
    time = models.DateTimeField(default=now)
    add_content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=1, choices=ACTION)
    image = models.ImageField(upload_to='status_images/%Y/%m/%d/', null=True)
    set_comments = GenericRelation('comments.Comment')
