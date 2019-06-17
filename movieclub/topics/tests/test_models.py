from django.test import TestCase
from users.models import User
from topics.models import Topic
from django.utils.timezone import now


class TopicTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user1', password='user1@user')
        User.objects.create(username='user2', password='user2@user')
        User.objects.create(username='user3', password='user3@user')

    def setUp(self):
        self.t1 = Topic.objects.create(
            head='Brilliance of Dileesh Pothan',
            time=now(),
            description='something just like this',
            created_by=User.objects.get(id=1),
            tags='malayalam, maheshinte prathikaram',
        )
        self.t1.save()

    def test_follow_the_topic(self):
        u = User.objects.get(id=2)
        self.t1.follow_the_topic(u)
        a = self.t1.followers.all()
        self.assertEqual(list(a), [u])
        self.t1.un_follow_the_topic(u)
        a = self.t1.followers.all()
        self.assertEqual(a.count(), 0)

    def test_watched(self):
        self.t1.watched()
        self.t1.watched()
        self.assertEqual(self.t1.no_of_watches, 2)
