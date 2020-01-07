import datetime
import uuid

from django.conf import settings
from django.db import models


# Create your models here.

class SocialMedia(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    facebook = models.URLField(null=True)
    twitter = models.URLField(null=True)
    instagram = models.URLField(null=True)


class StarQuerySet(models.query.QuerySet):
    pass


class Star(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='', default='', blank=True)
    social_media = models.OneToOneField(SocialMedia, on_delete=models.PROTECT,
                                        related_name='star', null=True)
    biography = models.TextField(blank=True, null=True)
    objects = StarQuerySet.as_manager()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_stars')
    updated_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='updated_stars')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='following_stars', blank=True)

    @property
    def get_age(self):
        current = datetime.datetime.now().year
        dob = self.date_of_birth.year
        return current - dob

    def follow(self, user):
        if not self.check_following(user):
            self.followers.add(user)
            self.save()

    def un_follow(self, user):
        if self.check_following(user):
            self.followers.remove(user)
            self.save()

    def check_following(self, user):
        return user in self.followers.all()

    def get_followers(self):
        return self.followers.all()

    def __str__(self):
        return self.name
