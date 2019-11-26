import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from movies.models import Movie
from topics.models import Topic


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
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(default=now, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    watched = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS, default='D')
    tags = TaggableManager(blank=True)
    contents = MarkdownxField()
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="%(class)s_liked", blank=True)
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name="%(class)s_disliked", blank=True)
    suggestion = GenericRelation('suggestions.Suggestion')
    objects = ContentQuerySet.as_manager()
    share_object = GenericRelation('shares.Share')
    image = models.ImageField(upload_to='contents/%(class)/%Y/%m/%d', null=True,
                              blank=True)
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
        return markdownify(self.contents)

    def get_comments(self):
        return self.set_comments.order_by('-time')


class Answer(Content):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ("-time",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.topic)

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
                self.user.email, self.movie.name, self.movie.released_year))
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
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(default=now, editable=False)
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=1, choices=ACTION)
    image = models.ImageField(upload_to='status_images/%Y/%m/%d/', null=True)
    set_comments = GenericRelation('comments.Comment')

    def get_comments(self):
        comments = self.set_comments.order_by('-time')
        return comments
