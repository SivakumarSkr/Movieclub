from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

from django.conf import settings
from persons.models import Star


# Create your models here.
from users.models import User


class MovieQuerySet(models.query.QuerySet):

    def get_by_year(self, year):

        if (int(year)) >= 1900 and (int(year) <= datetime.date.today().year):
            qs = self.filter(released_year=year)
        else:
            qs = None
        return qs

    def get_by_director(self, director):
        return self.filter(director=director)

    @staticmethod
    def get_by_stars(star):
        return star.movies_star.all()

    def get_by_language(self, language=None):
        return self.filter(language=language)

    @staticmethod
    def get_by_genre(genre):
        return genre.movies_genre.all()

    @staticmethod
    def get_by_writer(writer):
        return writer.movies_writer.all()


class Genre(models.Model):
    name = models.CharField(max_length=20)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Language(models.Model):
    name = models.CharField(max_length=20)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Movie(models.Model):
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
    writers = models.ManyToManyField(Star, related_name='movies_writer')
    stars = models.ManyToManyField(Star, related_name='movies_star')
    # thumbnail = models.ImageField()
    suggestion = GenericRelation('suggestions.Suggestion')
    objects = MovieQuerySet.as_manager()


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_ratings')
    rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
