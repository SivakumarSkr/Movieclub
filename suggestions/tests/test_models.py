import datetime
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
# from users.models import User
from movies.models import Movie, Language, Genre
from persons.models import Star, SocialMedia
from suggestions.models import Suggestion

User = get_user_model()


class SuggestionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='user1@gmail.com', password='user1@user1')
        User.objects.create(email='user2@gmail.com', password='user2@user2')
        User.objects.create(email='user3@gmail.com', password='user2@user3')
        User.objects.create(email='user4@gmail.com', password='user2@user4')
        Language.objects.create(name='English')
        Genre.objects.create(name='Thriller')
        Genre.objects.create(name='Sci-fi')
        SocialMedia.objects.create(
            facebook='https://facebook.com',
            twitter='https://twitter.com',
            instagram='https://instagram.com',
        )
        SocialMedia.objects.create(
            facebook='https://facebook.com',
            twitter='https://twitter.com',
            instagram='https://instagram.com',
        )
        social = SocialMedia.objects.all()
        Star.objects.create(
            name='Lio jos pallissery',
            date_of_birth=datetime.datetime(1973, 2, 4),
            country='India',
            social_media=social[0],
            biography='he is well known director in malayalam',

        )
        Star.objects.create(
            name='Dileesh pothan',
            date_of_birth=datetime.datetime(1969, 12, 12),
            country='India',
            social_media=social[1],
            biography='he is well known director in malayalam',

        )
        language = Language.objects.all()
        star = Star.objects.all()
        Movie.objects.create(
            name='Interstellar',
            released_year=2014,
            language=language[0],
            country='America',
            director=star[0],
        )
        Movie.objects.create(
            name='Memento',
            released_year=2000,
            language=language[0],
            country='America',
            director=star[0],
        )

    def setUp(self):
        self.users = User.objects.all()
        self.movies = Movie.objects.all()
        self.s1 = Suggestion.objects.create(
            sender=self.users[0],
            receiver=self.users[1],
            content_object=self.movies[0],
        )
        self.s2 = Suggestion.objects.create(
            sender=self.users[2],
            receiver=self.users[1],
            content_object=self.movies[1],
        )

    def test_check(self):
        self.assertEqual(list(self.movies[0].suggestions.all()), [self.s1])

    def test_get_sender_suggest(self):
        a = Suggestion.objects.get_suggestions_as_sender(self.users[2])
        b = Suggestion.objects.get_suggestions_as_sender(self.users[1])
        self.assertEqual(list(a), [self.s2])
        self.assertEqual(list(b), [])

    def test_get_receiver_suggest(self):
        a = Suggestion.objects.get_suggestions_as_receiver(self.users[2])
        b = Suggestion.objects.get_suggestions_as_receiver(self.users[1])
        self.assertEqual(a.count(), 0)
        self.assertEqual(b.count(), 2)
