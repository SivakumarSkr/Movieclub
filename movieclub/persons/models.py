import datetime

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

    @property
    def get_age(self):
        current = datetime.datetime.now().year
        dob = self.date_of_birth.year
        return current - dob
