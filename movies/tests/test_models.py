import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from movies.models import Genre, Language, Movie, Rating
from persons.models import Star, SocialMedia

User = get_user_model()


class MovieTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='user1@gmail.com', PASSWORD='user1@user')
        User.objects.create(email='user2@gmail.com', password='user2@user')
        User.objects.create(email='user3@gmail.com', password='user3@user')
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
        Star.objects.create(
            name='Shyam pushkar',
            date_of_birth=datetime.datetime(1983, 1, 22),
            country='India',
            social_media=social[2],
            biography='he is well known writer in malayalam',

        )
        Star.objects.create(
            name='Murali gopi',
            date_of_birth=datetime.datetime(1981, 11, 27),
            country='India',
            social_media=social[3],
            biography='he is well known writer in malayalam',
        )
        Star.objects.create(
            name='Fahad fasil',
            date_of_birth=datetime.datetime(1984, 11, 27),
            country='India',
            social_media=social[4],
            biography='he is well known writer in malayalam',
        )
        Star.objects.create(
            name='Prithviraj',
            date_of_birth=datetime.datetime(1983, 11, 27),
            country='India',
            social_media=social[5],
            biography='he is well known actor in malayalam',
        )

    def setUp(self):
        self.user = User.objects.all()
        self.stars = Star.objects.all()
        self.languages = Language.objects.all()
        self.genre = Genre.objects.all()
        self.movie1 = Movie(
            name='Angamaly diaries',
            released_year=2017,
            language=self.languages[0],
            country='India',
            director=self.stars[0],

        )
        self.movie1.writers.add(self.stars[2])
        self.movie1.writers.add(self.stars[3])
        self.movie1.stars.add(self.stars[4])
        self.movie1.stars.add(self.stars[5])
        self.movie1.genre.add(self.genre[0])
        self.movie1.genre.add(self.genre[1])
        self.movie1.save()
        self.movie2 = Movie(
            name='Sudani from Nigeria',
            released_year=2018,
            language=self.languages[0],
            country='India',
            director=self.stars[1],
        )
        self.movie2.writers.add(self.stars[2])
        self.movie2.writers.add(self.stars[3])
        self.movie2.stars.add(self.stars[4])
        self.movie2.stars.add(self.stars[5])
        self.movie2.genre.add(self.genre[0])
        self.movie2.save()
        self.movie3 = Movie(
            name='ee ma yau',
            released_year=2018,
            language=self.languages[0],
            country='India',
            director=self.stars[0],
        )
        self.movie3.writers.add(self.stars[2])
        self.movie3.stars.add(self.stars[4])
        self.movie3.genre.add(self.genre[0])
        self.movie3.save()
        self.r1 = Rating.objects.create(
            movie=self.movie1,
            user=self.user[0],
            rate=9,
        )
        self.r2 = Rating.objects.create(
            movie=self.movie1,
            user=self.user[1],
            rate=8,
        )
        self.r3 = Rating.objects.create(
            movie=self.movie1,
            user=self.user[2],
            rate=10,
        )

    def test_get_by_year(self):
        q = Movie.objects.get_by_year(2018)
        self.assertEqual(q.count(), 2)
        q = Movie.objects.get_by_year(1899)
        self.assertEqual(q, None)

    def test_get_by_director(self):
        q = Movie.objects.get_by_director(self.stars[0])
        self.assertEqual(q.count(), 2)
        q = Movie.objects.get_by_director(self.stars[1])
        self.assertEqual(list(q), [self.movie2])

    # def test_get_by_star(self):
    #     q = Movie.objects.get_by_stars(Star.objects.get(id=1))
    #     self.assertEqual(q.count(), 0)
    #     q = Movie.objects.get_by_stars(Star.objects.get(id=6))
    #     self.assertEqual(list(q), [self.movie1, self.movie2])

    def test_get_by_language(self):
        q = Movie.objects.get_by_language(self.languages[0])
        self.assertEqual(q.count(), 3)

    def test_language(self):
        self.assertEqual(str(self.languages[0]), 'malayalam')
        self.languages[0].follow(self.user[1])
        self.languages[0].follow(self.user[2])
        self.assertEqual(self.languages[0].check_following(self.user[1]), True)
        self.assertEqual(self.languages[0].check_following(self.user[0]), False)
        self.languages[0].un_follow(self.user[1])
        self.assertEqual(self.languages[0].check_following(self.user[1]), False)

    def test_genre(self):
        self.assertEqual(str(self.genre[0]), 'comedy')
        self.genre[0].follow(self.user[1])
        self.genre[0].follow(self.user[2])
        self.assertEqual(self.genre[0].check_following(self.user[1]), True)
        self.assertEqual(self.genre[0].check_following(self.user[0]), False)
        self.genre[0].un_follow(self.user[1])
        self.assertEqual(self.genre[0].check_following(self.user[1]), False)

    def test_get_by_genre(self):
        q = Movie.objects.get_by_genre(self.genre[0])
        self.assertEqual(q.count(), 3)
        q = Movie.objects.get_by_genre(self.genre[1])
        self.assertEqual(list(q), [self.movie1])

    # def test_get_by_writer(self):
    #     q = Movie.objects.get_by_writer(Star.objects.get(id=3))
    #     self.assertEqual(q.count(), 3)
    #     q = Movie.objects.get_by_writer(Star.objects.get(id=5))
    #     self.assertEqual(q.count(), 0)

    def test_rate(self):
        self.assertEqual(self.movie1.rating, 9)

    def test_movie(self):
        self.assertEqual(str(self.movie1), 'Angamaly diaries')
        self.assertEqual(self.movie1.get_stars().count(), 2)
        self.assertEqual(self.movie1.get_writers().count(), 2)
