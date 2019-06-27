import datetime

from django.conf import settings
from django.db import models


# Create your models here.

class SocialMedia(models.Model):
    facebook = models.URLField(null=True)
    twitter = models.URLField(null=True)
    instagram = models.URLField(null=True)


class StarQuerySet(models.query.QuerySet):
    pass


class Star(models.Model):
    name = models.CharField(max_length=30, blank=False)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='', default='', blank=True)
    social_media = models.OneToOneField(SocialMedia, on_delete=models.PROTECT,
                                        related_name='star', null=True)
    biography = models.TextField()
    objects = StarQuerySet.as_manager()
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_query_name='following_stars')

    @property
    def get_age(self):
        current = datetime.datetime.now().year
        dob = self.date_of_birth.year
        return current - dob

    def follow(self, user):
        self.followers.add(user)
        self.save()

    def un_follow(self, user):
        self.followers.remove(user)
        self.save()

    def check_following(self, user):
        return user in self.followers.all()

