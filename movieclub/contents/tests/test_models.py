from django.test import TestCase
from users.models import User
from contents.models import Answer, Review
from django.utils.timezone import now
from topics.models import Topic


class AnswerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user1', password='user1@user')
        User.objects.create(username='user2', password='user1@user')
        User.objects.create(username='userl', password='user2@user')
        User.objects.create(username='userd', password='user3@user')
        User.objects.create(username='usert', password='user4@user')
        User.objects.create(username='usert2', password='user4@user')
        user = User.objects.all()
        Topic.objects.create(
            head='interstellar decoding',
            time=now(),
            created_by=user[0],
        )
        Topic.objects.create(
            head='memento decoding',
            time=now(),
            created_by=user[0],
        )

    def setUp(self):
        self.user = User.objects.all()
        self.topic = Topic.objects.all()
        self.b1 = Answer.objects.create(
            time=now(),
            user=self.user[1],
            contents='this is just a begining',
            topic=self.topic[0],
        )
        self.b2 = Answer.objects.create(
            time=now(),
            user=self.user[2],
            contents='this is another begining',
            topic=self.topic[1],
        )

    def test_content_watched(self):
        self.b1.content_watched()
        self.assertEqual(self.b1.watched, 1)
        self.assertEqual(self.b2.watched, 0)

    def test_like_the_content(self):
        self.b1.like_the_content(self.user[4])
        self.assertEqual(self.b1.liked.all()[0], self.user[4])

    def test_dislike_the_content(self):
        self.b2.dislike_the_content(self.user[3])
        self.assertEqual(self.b2.disliked.all()[0], self.user[3])

    def test_both_like_dislike(self):
        self.b1.like_the_content(self.user[4])
        self.b1.dislike_the_content(self.user[4])
        self.assertEqual(self.b1.disliked.all()[0], self.user[4])
        self.assertEqual(self.b1.liked.all().count(), 0)
        self.b2.dislike_the_content(self.user[3])
        self.b2.like_the_content(self.user[3])
        self.assertEqual(self.b2.liked.all()[0], self.user[3])
        self.assertEqual(self.b2.disliked.all().count(), 0)

    def test_get_liked(self):
        self.b1.like_the_content(self.user[4])
        self.b1.like_the_content(self.user[5])
        self.assertEqual(self.b1.get_likes(), 2)
        self.b1.dislike_the_content(self.user[5])
        self.assertEqual(self.b1.get_likes(), 1)

    def test_get_disliked(self):
        self.b1.dislike_the_content(self.user[2])
        self.b1.dislike_the_content(self.user[3])
        self.assertEqual(self.b1.get_dislike(), 2)
        self.b1.like_the_content(self.user[2])
        self.assertEqual(self.b1.get_dislike(), 1)

    def test_content(self):
        self.assertEqual(self.b1.contents, 'this is just a begining')
