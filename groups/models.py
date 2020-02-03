import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from contents.models import Content


# Create your models here.
class GroupQuerySet(models.QuerySet):

    def create(self, **kwargs):
        kwargs['type_of_group'] = 'O'
        return super().create(**kwargs)

    def get_open(self):
        return self.filter(type_of_group='O')

    def created_by(self, user):
        query = self.filter(creator=user)
        return query

    def admin_by(self, user):
        query = self.filter(admins=user)
        return query


class Group(models.Model):
    OPEN = 'O'
    CLOSED = 'C'
    TYPE = ((OPEN, 'Open'),
            (CLOSED, 'Closed'))

    uuid_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField('Name', max_length=30)
    time_created = models.DateTimeField(default=now)
    description = models.TextField(max_length=500)
    type_of_group = models.CharField('Type', choices=TYPE, max_length=1)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='groups_admin', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='groups_joined', blank=True)
    objects = GroupQuerySet.as_manager()

    def __str__(self):
        return self.name

    def join(self, user):
        if not self.check_member(user):
            self.members.add(user)
            self.save()

    def leave(self, user):
        if self.check_member(user):
            self.members.remove(user)
            self.save()

    def check_member(self, user):
        return user in self.members.all()

    def get_members(self):
        return self.members.all()

    def get_group_blog(self):
        return self.blogs.order_by('-time')

    def is_creator(self, user):
        return self.creator == user


class ClosedGroupManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(type_of_group='C')

    def create(self, **kwargs):
        kwargs['type_of_group'] = 'C'
        return super().create(**kwargs)


class ClosedGroup(Group):
    objects = ClosedGroupManager()

    def add_admin(self, user):
        if not self.is_admin(user):
            self.admins.add(user)
            self.save()

    def remove_admin(self, user):
        if self.is_admin(user):
            self.admins.remove(user)
            self.save()

    def get_admins(self):
        return self.admins.all()

    def is_admin(self, user):
        admins = self.get_admins()
        if admins.filter(pk=user.pk).exists() or user == self.creator:
            return True

    class Meta:
        proxy = True

    def is_admin(self, user):
        admins = self.get_admins()
        if admins.filter(pk=user.pk).exists() or user == self.creator:
            return True

    class Meta:
        proxy = True


class GroupBlog(Content):
    heading = models.CharField(max_length=300)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='blogs')
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.heading

    def make_published(self):
        self.published = True
        self.save()


class JoinRequest(models.Model):
    uuid_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    group = models.ForeignKey(
        'groups.ClosedGroup', on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='join_requests')
    authorizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='authorized_requests')
    requested_time = models.DateTimeField(auto_now_add=True, editable=False)
    is_approved = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def approve(self, user):
        self.group.join(self.user)
        self.is_approved = True
        self.authorizer = user
        self.save()

    def cancel(self, user):
        self.authorizer = user
        self.is_cancelled = True
        self.save()
