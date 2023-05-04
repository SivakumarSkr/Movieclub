import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_prime = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    contact_no = PhoneNumberField(null=True)
    place = models.CharField(max_length=20, null=True)
    followers = models.ManyToManyField('self', symmetrical=False,
                                       related_name='following', blank=True)
    watched_films = models.ManyToManyField('movies.Movie', blank=True)
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def follow(self, user):
        self.followers.add(user)
        self.save()

    def un_follow(self, user):
        self.followers.remove(user)
        self.save()

    def get_followers(self):
        qs = self.followers.all()
        return qs

    def get_following(self):
        qs = self.following.all()
        return qs

    @property
    def get_number_followers(self):
        return self.followers.all().count()

    @property
    def get_number_following(self):
        return self.following.all().count()

    def get_followed_topics(self):
        return self.topics_followed.all()

    def get_drafted_blog(self):
        return self.blog_set.filter(status='D').order_by('-time')

    def get_drafted_review(self):
        return self.review_set.filter(status='D').order_by('-time')

    def get_drafted_answer(self):
        return self.answer_set.filter(status='D').order_by('-time')

    def get_published_blog(self):
        return self.blog_set.filter(status='P').order_by('-time')

    def get_published_review(self):
        return self.review_set.filter(status='P').order_by('-time')

    def get_published_answer(self):
        return self.answer_set.filter(status='P').order_by('-time')

    def get_following_groups(self):
        return self.groups_followed.all()

    def get_watched_films(self):
        return self.watched_films.all()

    def check_watched(self, movie):
        return self.watched_films.all().filter(pk=movie.pk).exists()

    def get_following_stars(self):
        return self.following_stars.all()

    def get_suggestions_received(self):
        return self.suggest_receiver.order_by('-time')

    def get_suggestions_sent(self):
        return self.suggest_sender.order_by('-time')

    def get_common_followers(self, user):
        query = self.get_following().intersection(user.get_following())
        return query

    def get_common_groups(self, user):
        query = self.get_following_groups().intersection(user.get_following_groups())
        return query

    def get_common_star_followers(self, user):
        query = self.get_following_stars().intersection(user.get_following_stars())
        return query

    def get_notifications_unread(self):
        query = self.notifications.filter(unread=True)
        return query

    def get_notifications_read(self):
        query = self.notifications.filter(unread=False)
        return query
