import datetime
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from persons.models import Star
from suggestions.models import Suggestion

# Create your models here.
# from users.models import User

User = get_user_model()


def upload_to_movies(instance, filename):
    return 'images/{}/{}/{}'.format(instance.name, instance.released_year, filename)


def upload_to(instance, filname):
    return 'images/{}/{}/{}'.format('%(class)', instance.name, filname)


class MovieQuerySet(models.query.QuerySet):

    def get_by_year(self, year):

        if (int(year)) >= 1900 and (int(year) <= datetime.date.today().year):
            qs = self.filter(released_year=year)
        else:
            qs = None
        return qs

    def get_by_director(self, director):
        return self.filter(director=director)

    def get_by_language(self, language=None):
        return self.filter(language=language)

    def get_by_genre(self, genre):
        return self.filter(genre=genre)


class Genre(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=20)
    thumbnail = models.ImageField(upload_to=upload_to, null=True, blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name

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


class Language(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=20)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    thumbnail = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return self.name

    def check_following(self, user):
        return user in self.followers.all()

    def follow(self, user):
        if not self.check_following(user):
            self.followers.add(user)
            self.save()

    def un_follow(self, user):
        if self.check_following(user):
            self.followers.remove(user)
            self.save()


class Movie(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    released_year = models.IntegerField(validators=
                                        [MinValueValidator(1900),
                                         MaxValueValidator(datetime.date.today().year)])
    language = models.ForeignKey(Language, on_delete=models.PROTECT,
                                 related_name='movies_language')
    genre = models.ManyToManyField(Genre, related_name='movies_genre')
    country = models.CharField(max_length=40)
    director = models.ForeignKey(Star, on_delete=models.PROTECT,
                                 related_name='movies_director')
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10),
                                                                MinValueValidator(0)])
    writers = models.ManyToManyField(Star, related_name='movies_writer')
    stars = models.ManyToManyField(Star, related_name='movies_star')
    thumbnail = models.ImageField(upload_to=upload_to_movies, null=True)
    suggestions = GenericRelation(Suggestion, related_query_name='movie_suggestion')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_movies')
    updated_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='updated_movies')
    objects = MovieQuerySet.as_manager()

    def __str__(self):
        return self.name

    def set_rate(self, rate):
        ave_rate = (self.rating * self.number_of_rates + rate) / self.number_of_rates + 1
        self.rating = int(ave_rate)
        self.save()

    def get_stars(self):
        return self.stars.all()

    def get_writers(self):
        return self.writers.all()

    @property
    def number_of_rates(self):
        return self.ratings.count()


class Rating(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_ratings')
    rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10),
                                                        MinValueValidator(0)])


@receiver(signals.post_save, sender=Rating)
def rate_the_movie(sender, instance, created, **kwargs):
    movie_obj = instance.movie
    movie_obj.set_rate(instance.rate)
