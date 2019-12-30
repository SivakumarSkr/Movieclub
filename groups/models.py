import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from contents.models import Content


# Create your models here.
class GroupQuerySet(models.QuerySet):
    def get_closed(self):
        return self.filter(type_of_group='C')

    def get_open(self):
        return self.filter(type_of_group='O')

    def created_by(self, user):
        query = self.filter(creator=user)
        return query

    def admin_by(self, user):
        query = self.filter(admins=user)
        return query


class Group(models.Model):
    CLOSED = 'C'
    OPEN = 'O'
    TYPE = (
        (CLOSED, 'Closed'),
        (OPEN, 'Open')
    )
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField('Name', max_length=30)
    time_created = models.DateTimeField(default=now)
    type_of_group = models.CharField(max_length=1, choices=TYPE, default='O')
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='groups_admin', blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='groups_followed', blank=True)
    objects = GroupQuerySet.as_manager()

    def __str__(self):
        return self.name

    def follow(self, user):
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

    def get_admins(self):
        return self.admins.all()

    def get_group_blog(self):
        return self.blogs.order_by('-time')

    def check_closed(self):
        return self.type_of_group == 'C'

    def add_admin(self, user):
        self.admins.add(user)
        self.save()

    def is_admin(self, user):
        admins = self.get_admins()
        if admins.filter(pk=user.pk).exists() or user == self.creator:
            return True


class GroupBlog(Content):
    heading = models.CharField(max_length=300)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='blogs')
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.heading

    def make_published(self):
        self.published = True
        self.save()


class JoinRequest(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='join_requests')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name='approved_requests')
    requested_time = models.DateTimeField(auto_now_add=True, editable=False)
    is_approved = models.BooleanField(default=False)

    def approve(self, user):
        if self.group.is_admin(user):
            self.is_approved = True
            self.save()
