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
            date_of_birth=datetime.datetime(1995, 6, 1),
            country='indian',
            social_media=self.social[0],
            biography='He is good film director',
        )
        self.star2 = Star.objects.create(
            name='Lijo jose pallissery',
            date_of_birth=datetime.datetime(1992, 6, 1),
            country='indian',
            social_media=self.social[1],
            biography='jsdfalkjfdsa',
        )

    def test_get_age(self):
        self.assertEqual(self.star1.get_age, 24)

    def test_follow(self):
        self.star1.follow(self.user[0])
        self.star1.follow(self.user[1])
        self.assertEqual(self.star1.get_followers().count(), 2)
        self.assertEqual(self.star1.check_following(self.user[0]), True)
        self.assertEqual(self.star1.check_following(self.user[2]), False)
        self.star1.un_follow(self.user[0])
        self.assertEqual(self.star1.check_following(self.user[0]), False)
