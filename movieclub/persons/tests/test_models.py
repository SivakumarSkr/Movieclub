import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings
from movies.models import Movie, Language, Genre
from persons.models import Star, SocialMedia

User = get_user_model()


class PersonTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user2', password='user4')
        User.objects.create(username='user4', password='user4')
        User.objects.create(username='user6', password='user4')
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

    def setUp(self):
        self.social = SocialMedia.objects.all()
        self.user = User.objects.all()
        self.star1 = Star.objects.create(
            name='Lijo jose pallissery',
            date_of_birth=datetime.datetime,
            country='indian',
            social_media=self.social[0],
            biography='He is good film director',
        )
        self.star2 = Star.objects.create(
            name='Lijo jose pallissery',
            date_of_birth='23-4-1978',
            country='indian',
            social_media=self.social[1],
            biography='jsdfalkjfdsa',
        )

    # def test_get_age(self):
    #     self.assertEqual(self.star1.get_age(), 41)
