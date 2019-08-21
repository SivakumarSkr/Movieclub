from django.contrib.auth import get_user_model
from django.test import TestCase
# from users.models import User
from topics.models import Topic
from django.utils.timezone import now

User = get_user_model()


class TopicTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='user1@gmail.com', password='user1@user')
        User.objects.create(email='user2@gmail.com', password='user2@user')
        User.objects.create(email='user3@gmail.com', password='user3@user')

    def setUp(self):
        self.users = User.objects.all()
        self.t1 = Topic.objects.create(
            head='Brilliance of Dileesh Pothan',
            time=now(),
            description='something just like this',
            created_by=self.users[0],
            tags='malayalam, maheshinte prathikaram',
        )
        self.t2 = Topic.objects.create(
            head='Brilliance of Dileesh Pothan',
            time=now(),
            description='something just like this',
            created_by=self.users[1],
            tags='malayalam, maheshinte prathikaram',
        )

    def test_follow_the_topic(self):
        self.t1.follow_the_topic(self.users[1])
        a = self.t1.followers.all()
        self.assertEqual(list(a), [self.users[1]])
        self.t1.un_follow_the_topic(self.users[1])
        a = self.t1.followers.all()
        self.assertEqual(a.count(), 0)

    def test_watched(self):
        self.t1.watched()
        self.t1.watched()
        self.assertEqual(self.t1.no_of_watches, 2)

    def test_get_latest(self):
        a = Topic.objects.get_latest_topics()
        self.assertEqual(list(a), [self.t2, self.t1])

    def test_get_trending(self):
        trend = Topic.objects.get_trending()
        self.assertEqual(trend[0], self.t1)
        self.t2.watched()
        self.t2.watched()
        self.t2.watched()
        print(self.t2.no_of_watches)
        trend = Topic.objects.get_trending()
        self.assertEqual(trend[0], self.t2)

    # def test_get_most_followed(self):
    #     print(Topic.objects.get_most_followed())
