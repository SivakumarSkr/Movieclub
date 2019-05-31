from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from movieclub.contents.models import Content


# Create your models here.
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
        return star.movies.all()

    def get_by_language(self, language=None):
        return self.filter(language=language)

    @staticmethod
    def get_by_genre(genre):
        return genre.movies.all()

    @staticmethod
    def get_by_writer(writer):
        return writer.movies.all()


class Genre(models.Model):
    name = models.CharField(max_length=20)
    # followers = models.ManyToManyField('User')


class Language(models.Model):
    name = models.CharField(max_length=20)
    # followers = models.ManyToManyField('User')


class Movie(models.Model):
    name = models.CharField(max_length=30)
    released_year = models.IntegerField(validators=
                                        [MinValueValidator(1900),
                                         MaxValueValidator(datetime.date.today().year)])
    language = models.ForeignKey(Language, on_delete=models.PROTECT,
                                 related_name='movies')
    genre = models.ManyToManyField(Genre, related_name='movies')
    country = models.CharField(max_length=40)
    director = models.ForeignKey(Star, on_delete=models.PROTECT, related_name='movie')
    writers = models.ManyToManyField(Star, related_name='movie')
    stars = models.ManyToManyField(Star, related_name='movie')
    # thumbnail = models.ImageField()
    objects = MovieQuerySet.as_manager()
