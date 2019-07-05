import datetime

from django.test import TestCase
from users.models import User
import pytest
from topics.models import Topic

from contents.models import Blog

from contents.models import Review
from movies.models import Genre, Language, Movie
from persons.models import Star, SocialMedia

from contents.models import Answer

from groups.models import Group

from suggestions.models import Suggestion


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='comedy')
        Genre.objects.create(name='thriller')
        Language.objects.create(name='malayalam')
        Language.objects.create(name='tamil')
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
        languages = Language.objects.all()
        socails = SocialMedia.objects.all()
        genre = Genre.objects.all()
        Star.objects.create(
            name='Lio jos pallissery',
            date_of_birth=datetime.datetime(1973, 2, 4),
            country='India',
            social_media=socails[0],
            biography='he is well known director in malayalam',

        )
        Star.objects.create(
            name='Dileesh pothan',
            date_of_birth=datetime.datetime(1969, 12, 12),
            country='India',
            social_media=socails[1],
            biography='he is well known director in malayalam',

        )
        Star.objects.create(
            name='Shyam pushkar',
            date_of_birth=datetime.datetime(1983, 1, 22),
            country='India',
            social_media=socails[2],
            biography='he is well known writer in malayalam',

        )
        Star.objects.create(
            name='Murali gopi',
            date_of_birth=datetime.datetime(1981, 11, 27),
            country='India',
            social_media=socails[3],
            biography='he is well known writer in malayalam',
        )
        Star.objects.create(
            name='Fahad fasil',
            date_of_birth=datetime.datetime(1984, 11, 27),
            country='India',
            social_media=socails[4],
            biography='he is well known writer in malayalam',
        )
        Star.objects.create(
            name='Prithviraj',
            date_of_birth=datetime.datetime(1983, 11, 27),
            country='India',
            social_media=socails[5],
            biography='he is well known actor in malayalam',
        )
        stars = Star.objects.all()
        movie1 = Movie(
            name='Angamaly diaries',
            released_year=2017,
            language=languages[0],
            country='India',
            director=stars[0],

        )
        movie1.writers.add(stars[2])
        movie1.writers.add(stars[3])
        movie1.stars.add(stars[4])
        movie1.stars.add(stars[5])
        movie1.genre.add(genre[0])
        movie1.genre.add(genre[1])
        movie1.save()
        movie2 = Movie(
            name='Sudani from Nigeria',
            released_year=2018,
            language=languages[0],
            country='India',
            director=stars[1],
        )
        movie2.writers.add(stars[2])
        movie2.writers.add(stars[3])
        movie2.stars.add(stars[4])
        movie2.stars.add(stars[5])
        movie2.genre.add(genre[0])
        movie2.save()

    def setUp(self):
        self.movies = Movie.objects.all()
        self.stars = Star.objects.all()
        self.user1 = User.objects.create(username='user1', password='user1@user')
        self.user2 = User.objects.create(username='user2', password='user2@user')
        self.user3 = User.objects.create(username='user3', password='user3@user')
        self.t1 = Topic.objects.create(
            head='brilliance of dileesh',
            created_by=self.user1,
        )
        self.t1.followers.add(self.user2)
        self.t1.save()

        self.t2 = Topic.objects.create(
            head='brilliance of lijo',
            created_by=self.user1,
        )
        self.t2.followers.add(self.user2)
        self.t2.save()
        self.b1 = Blog.objects.create(
            user=self.user1,
            status='D',
            heading="something just like this",
        )
        self.b2 = Blog.objects.create(
            user=self.user1,
            status='D',
            heading="something just like this1",
        )
        self.r1 = Review.objects.create(
            user=self.user3,
            status='D',
            movie=self.movies[1],
        )

        self.r2 = Review.objects.create(
            user=self.user3,
            status='D',
            movie=self.movies[0]
        )
        self.a1 = Answer.objects.create(
            user=self.user2,
            status='D',
            topic=self.t2,
        )
        self.a2 = Answer.objects.create(
            user=self.user2,
            status='D',
            topic=self.t1,
        )
        self.g1 = Group.objects.create(
            name='korean lovers',
            creator=self.user2,
        )
        self.g1.followers.add(self.user1)
        self.g1.save()
        self.g2 = Group.objects.create(
            name='spanish lovers',
            creator=self.user3,
        )
        self.g2.followers.add(self.user1)
        self.g2.save()

        self.user1.watched_films.add(
            self.movies[0], self.movies[1]
        )
        self.user3.following_stars.add(self.stars[2], self.stars[1])
        self.stars[3].followers.add(self.user3)
        self.user1.save()

        self.s1 = Suggestion.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content_object=self.movies[1],
        )
        self.s2 = Suggestion.objects.create(
            sender=self.user3,
            receiver=self.user2,
            content_object=self.r1,
        )
        self.b1p = Blog.objects.create(
            user=self.user2,
            status='P',
            heading="something just like this",
        )
        self.b2p = Blog.objects.create(
            user=self.user2,
            status='P',
            heading="something just like this1",
        )
        self.r1p = Review.objects.create(
            user=self.user1,
            status='P',
            movie=self.movies[1],
        )

        self.r2p = Review.objects.create(
            user=self.user1,
            status='P',
            movie=self.movies[0]
        )
        self.a1p = Answer.objects.create(
            user=self.user3,
            status='P',
            topic=self.t2,
        )
        self.a2p = Answer.objects.create(
            user=self.user3,
            status='P',
            topic=self.t1,
        )

    def test_follow(self):
        self.user1.follow(self.user2)
        self.assertEqual(list(self.user1.followers.all()), [self.user2])
        self.assertEqual(list(self.user2.following.all()), [self.user1])
        self.assertEqual(self.user1.following.all().count(), 0)
        self.assertEqual(self.user2.followers.all().count(), 0)

    def test_un_follow(self):
        self.user1.follow(self.user2)
        self.user2.follow(self.user1)
        self.user2.unfollow(self.user1)
        self.assertEqual(list(self.user1.followers.all()), [self.user2])
        self.assertEqual(list(self.user2.following.all()), [self.user1])
        self.assertEqual(self.user1.following.all().count(), 0)
        self.assertEqual(self.user2.followers.all().count(), 0)

    def test_follow_one_side(self):
        self.user1.followers.add(self.user2)
        a = self.user1.followers.all()
        self.assertEqual(a[0], self.user2)
        b = self.user2.followers.all()
        self.assertEqual(b.count(), 0)
        c = self.user2.following.all()
        self.assertEqual(c[0], self.user1)
        d = self.user1.following.all()
        self.assertEqual(d.count(), 0)

    def test_follow_two_side(self):
        self.user1.followers.add(self.user2)
        self.user2.followers.add(self.user1)
        self.user3.followers.add(self.user1)
        self.assertEqual(list(self.user1.followers.all()), [self.user2])
        self.assertEqual(list(self.user2.followers.all()), [self.user1])
        self.assertEqual(list(self.user1.following.all()), [self.user2, self.user3])
        self.assertEqual(list(self.user2.following.all()), [self.user1])
        self.assertEqual(list(self.user3.followers.all()), [self.user1])

    def test_get_no_followers(self):
        self.user1.follow(self.user2)
        self.user1.follow(self.user3)
        self.assertEqual(self.user1.get_number_followers(), 2)
        self.assertEqual(self.user3.get_number_followers(), 0)
        self.assertEqual(self.user3.get_number_following(), 1)
        self.assertEqual(self.user3.get_number_following(), 1)

    def test_get_followers(self):
        self.user1.follow(self.user2)
        self.user1.follow(self.user3)
        self.assertEqual(list(self.user1.get_followers()), [self.user2, self.user3])
        self.assertEqual(list(self.user3.get_followers()), [])
        self.assertEqual(list(self.user3.get_following()), [self.user1])
        self.assertEqual(list(self.user1.get_following()), [])

    def test_get_followed_topics(self):
        a = self.user2.get_followed_topics()
        self.assertEqual(a.count(), 2)

    def test_get_drafted_blog(self):
        a = self.user1.get_drafted_blog()
        self.assertEqual(a.count(), 2)

    def test_get_drafted_review(self):
        a = self.user3.get_drafted_review()
        self.assertEqual(a.count(), 2)

    def test_get_drafted_answer(self):
        a = self.user2.get_drafted_answer()
        self.assertEqual(a.count(), 2)

    def test_get_followed_groups(self):
        a = self.user1.get_followed_groups()
        self.assertEqual(a.count(), 2)

    def test_get_watched_films(self):
        a = self.user1.get_watched_films()
        self.assertEqual(a.count(), 2)

    def test_get_followed_stars(self):
        a = self.user3.get_followed_stars()
        self.assertEqual(a.count(), 3)

    def test_get_suggestions_received(self):
        a = self.user2.get_suggestions_received()
        self.assertEqual(a.count(), 2)

    def test_get_published_blog(self):
        a = self.user2.get_published_blog()
        self.assertEqual(a.count(), 2)

    def test_get_published_review(self):
        a = self.user1.get_published_review()
        self.assertEqual(a.count(), 2)

    def test_get_published_answer(self):
        a = self.user3.get_published_answer()
        self.assertEqual(a.count(), 2)
