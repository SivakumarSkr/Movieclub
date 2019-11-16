from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _


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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=True)
    is_prime = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    contact_no = PhoneNumberField(null=True)
    place = models.CharField(max_length=20, null=True)
    followers = models.ManyToManyField('self', symmetrical=False,
                                       related_name='following', blank=True)
    watched_films = models.ManyToManyField('movies.Movie', blank=True)
    last_login = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
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

    def get_number_followers(self):
        return self.followers.all().count()

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

    def get_followed_groups(self):
        return self.groups_followed.all()

    def get_watched_films(self):
        return self.watched_films.all()

    def check_watched(self, movie):
        return movie in self.watched_films.all()

    def get_followed_stars(self):
        return self.following_stars.all()

    def get_suggestions_received(self):
        return self.suggest_receiver.order_by('-time')

    def get_suggestions_sent(self):
        return self.suggest_sender.order_by('-time')

