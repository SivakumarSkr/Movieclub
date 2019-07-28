from django.test import TestCase
from django.conf import settings
from movies.models import Movie, Language, Genre
from persons.models import Star

User = settings.AUTH_USER_MODEL


class PersonTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user2', password='user4')
        User.objects.create(username='user4', password='user4')
        User.objects.create(username='user6', password='user4')
        Language.objects.create(name='English')
        Genre.objects.create(name='Thriller')
        Genre.objects.create(name='Sci-fi')

    def setUp(self):
        self.user = User.objects.all()
        self.star1 = Star.objects.create(

        )
