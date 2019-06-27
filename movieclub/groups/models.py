import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from contents.models import Content


# Create your models here.
class GroupQuerySet(models.query.QuerySet):

    def get_followed_groups(self, user):
        return self.filter(followers=user)


class Group(models.Model):
    name = models.CharField('Name', max_length=30)
    time_created = models.DateTimeField(default=now)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='groups_admin', blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='groups_followed', blank=True)

    def __str__(self):
        return self.name

    def follow(self, user):
        self.followers.add(user)
        self.save()

    def un_follow(self, user):
        self.followers.remove(user)
        self.save()

    def check_following(self, user):
        return user in self.followers.all()

    def get_followers(self):
        return self.followers.all()

    def get_follower(self):
        return self.followers.all()

    def get_admins(self):
        return self.admins.all()


class GroupBlog(Content):
    uuid_ui = models.UUIDField(default=uuid.uuid4)
    heading = models.CharField(max_length=300)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='blog')

    def __str__(self):
        return self.heading
