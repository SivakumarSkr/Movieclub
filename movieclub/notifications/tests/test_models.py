from django.test import TestCase
# from django.conf import settings
from django.contrib.auth import get_user_model
from contents.models import Blog, Answer
from notifications.models import Notification

User = get_user_model()


class NotificationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user1', password='user4')
        User.objects.create(username='user2', password='user4')
        User.objects.create(username='user3', password='user4')
        User.objects.create(username='user4', password='user4')
        User.objects.create(username='user5', password='user4')
        users = User.objects.all()
        Blog.objects.create(
            user=users[0],
            heading='brilliance of virus',
        )
        Blog.objects.create(
            user=users[1],
            heading='brilliance of ishq',
        )

    def setUp(self):
        self.users = User.objects.all()
        self.not1 = Notification.objects.create(
            creator=self.users[1],
            receiver=self.users[2],
            category='L',
            subject_object=Blog.objects.all()[0],

        )
        self.not3 = Notification.objects.create(
            creator=self.users[1],
            receiver=self.users[2],
            category='L',
            unread=False,
            subject_object=Blog.objects.all()[0],

        )
        self.not2 = Notification.objects.create(
            creator=self.users[3],
            receiver=self.users[4],
            category='C',
            subject_object=Blog.objects.all()[1],
        )
        self.not4 = Notification.objects.create(
            creator=self.users[1],
            receiver=self.users[4],
            category='C',
            subject_object=Blog.objects.all()[1],
        )

    def test_get_unread(self):
        test = Notification.objects.get_unread(self.users[2])
        self.assertEqual(test.count(), 1)

    def test_get_read(self):
        test = Notification.objects.get_read(self.users[2])
        self.assertEqual(test.count(), 1)

    # def test_mark_all_as_read(self):
    #     Notification.objects.mark_all_as_read(self.users[4])
    #     self.assertEqual(self.not4.unread, False)
    #     self.assertEqual(self.not2.unread, False)
    #
    # def test_get_latest(self):
    #     test = Notification.objects.get_latest(self.users[4])
    #     self.assertEqual(test[0], self.not4)
