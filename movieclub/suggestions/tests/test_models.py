import datetime
import os
from django.test import TestCase
from users.models import User
from movies.models import Movie, Language, Genre
from persons.models import Star, SocialMedia
from suggestions.models import Suggestion


class SuggestionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user1', password='user1@user1')
        User.objects.create(username='user2', password='user2@user2')
        User.objects.create(username='user3', password='user2@user3')
        User.objects.create(username='user4', password='user2@user4')
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
        Star.objects.create(
            name='Lio jos pallissery',
            date_of_birth=datetime.datetime(1973, 2, 4),
            country='India',
            social_media=SocialMedia.objects.get(id=1),
            biography='he is well known director in malayalam',

        )
        Star.objects.create(
            name='Dileesh pothan',
            date_of_birth=datetime.datetime(1969, 12, 12),
            country='India',
            social_media=SocialMedia.objects.get(id=2),
            biography='he is well known director in malayalam',

        )
        Movie.objects.create(
            name='Interstellar',
            released_year=2014,
            language=Language.objects.get(id=1),
            country='America',
            director=Star.objects.get(id=1),
        )
        Movie.objects.create(
            name='Memento',
            released_year=2000,
            language=Language.objects.get(id=1),
            country='America',
            director=Star.objects.get(id=1),
        )

    def setUp(self):
        self.s1 = Suggestion.objects.create(
            sender=User.objects.get(id=1),
            receiver=User.objects.get(id=2),
            content_object=Movie.objects.get(id=1),
        )
        self.s1.save()
        self.s2 = Suggestion.objects.create(
            sender=User.objects.get(id=3),
            receiver=User.objects.get(id=2),
            content_object=Movie.objects.get(id=2),
        )
        self.s2.save()

    def test_check(self):
        self.assertEqual(list(Movie.objects.get(id=1).suggestions.all()), [self.s1])

    def test_get_sender_suggest(self):
        a = Suggestion.objects.get_suggestions_as_sender(User.objects.get(id=3))
        b = Suggestion.objects.get_suggestions_as_sender(User.objects.get(id=2))
        self.assertEqual(list(a), [self.s2])
        self.assertEqual(list(b), [])

    def test_get_receiver_suggest(self):
        a = Suggestion.objects.get_suggestions_as_receiver(User.objects.get(id=3))
        b = Suggestion.objects.get_suggestions_as_receiver(User.objects.get(id=2))
        self.assertEqual(a.count(), 0)
        self.assertEqual(b.count(), 2)



