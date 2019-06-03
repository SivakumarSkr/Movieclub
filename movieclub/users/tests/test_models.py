from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='user1@user')
        self.user2 = User.objects.create(username='user2', password='user2@user')
        self.user3 = User.objects.create(username='user3', password='user3@user')

    def test_follow(self):
        self.user1.follow(self.user2)
        self.assertEqual(list(self.user1.followers.all()), [self.user2])
        self.assertEqual(list(self.user2.following.all()), [self.user1])
        self.assertEqual(self.user1.following.all().count(), 0)
        self.assertEqual(self.user2.followers.all().count(), 0)

    def test_unfollow(self):
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

    def test_get_followers(self):
        self.user1.follow(self.user2)
        self.user1.follow(self.user3)
        self.assertEqual(self.user1.get_number_followers(), 2)
        self.assertEqual(self.user3.get_number_followers(), 0)
        self.assertEqual(self.user3.get_number_following(), 1)
        self.assertEqual(self.user3.get_number_following(), 1)

