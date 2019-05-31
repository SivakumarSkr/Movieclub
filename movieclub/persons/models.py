from django.db import models


# Create your models here.

class SocialMedia(models.Model):
    facebook = models.URLField(null=True)
    twitter = models.URLField(null=True)
    instagram = models.URLField(null=True)


# class StarQuerySet(models.query.QuerySet):
#     pass


class Star(models.Model):
    name = models.CharField(max_length=30, blank=False)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=30)
    # photo = models.ImageField()
    social_media = models.OneToOneField(SocialMedia, on_delete=models.PROTECT,
                                        related_name='star')
    biography = models.TextField()
    # objects = StarQuerySet.as_manager()
