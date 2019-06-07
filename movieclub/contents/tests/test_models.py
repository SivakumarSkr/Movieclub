from django.test import TestCase
from users.models import User
from contents.models import Answer, Review
from django.utils.timezone import now
from topics.models import Topic

class AnswerTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='user1@user')
        self.user2 = User.objects.create(username='user2', password='user1@user')
        self.liked_u = User.objects.create(username='userl', password='user2@user')
        self.disliked_u = User.objects.create(username='userd',password='user3@user')
        self.topic_user = User.objects.create(username='usert', password='user4@user')
        self.topic_user2 = User.objects.create(username='usert2', password='user4@user')
        self.topic1 = Topic.objects.create(
            head='interstellar decoding',
            time=now(),
            created_by=self.topic_user,
        )
        self.topic2 = Topic.objects.create(
            head='memento decoding',
            time=now(),
            created_by=self.topic_user,
        )
        self.b1 = Answer.objects.create(
            time=now(),
            user=self.user1,
            contents='this is just a begining',
            topic=self.topic1,
        )
        self.b2 = Answer.objects.create(
            time=now(),
            user=self.user2,
            contents='this is another begining',
            topic=self.topic2,
        )

    def test_content_watched(self):
        self.b1.content_watched()
        self.assertEqual(self.b1.watched, 1)
        self.assertEqual(self.b2.watched, 0)

    def test_like_the_content(self):
        self.b1.like_the_content(self.liked_u)
        self.assertEqual(self.b1.liked.all()[0], self.liked_u)

    def test_dislike_the_content(self):
        self.b2.dislike_the_content(self.disliked_u)
        self.assertEqual(self.b2.disliked.all()[0], self.disliked_u)

    def test_both_like_dislike(self):
        self.b1.like_the_content(self.liked_u)
        self.b1.dislike_the_content(self.liked_u)
        self.assertEqual(self.b1.disliked.all()[0], self.liked_u)
        self.assertEqual(self.b1.liked.all().count(), 0)
        self.b2.dislike_the_content(self.disliked_u)
        self.b2.like_the_content(self.disliked_u)
        self.assertEqual(self.b2.liked.all()[0], self.disliked_u)
        self.assertEqual(self.b2.disliked.all().count(), 0)

    def test_get_liked(self):
        self.b1.like_the_content(self.user1)
        self.b1.like_the_content(self.user2)
        self.assertEqual(self.b1.get_likes(), 2)
        self.b1.dislike_the_content(self.user2)
        self.assertEqual(self.b1.get_likes(), 1)

    def test_get_disliked(self):
        self.b1.dislike_the_content(self.user1)
        self.b1.dislike_the_content(self.user2)
        self.assertEqual(self.b1.get_dislike(), 2)
        self.b1.like_the_content(self.user2)
        self.assertEqual(self.b1.get_dislike(), 1)

