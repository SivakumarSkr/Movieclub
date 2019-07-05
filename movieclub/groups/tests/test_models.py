from django.test import TestCase

from users.models import User

from groups.models import Group


class GroupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user1', password='user1@123')
        User.objects.create(username='user2', password='user2@123')
        User.objects.create(username='user3', password='user1@123')
        User.objects.create(username='user4', password='user2@123')
        User.objects.create(username='user5', password='user1@123')
        User.objects.create(username='user6', password='user2@123')

    def setUp(self):
        self.g1 = Group.objects.create(
            name='korean lovers',
            description='something',
            creator=User.objects.get(id=1),
        )
        self.g1.admin.add(
            User.objects.get(id=2),
            User.objects.get(id=3)
        )
        self.g1.followers.add(
            User.objects.get(id=5),
            User.objects.get(id=6)
        )
        self.g1.save()
        self.g2 = Group.objects.create(
            name='korean lovers',
            description='something',
            creator=User.objects.get(id=2),
        )
        self.g2.admin.add(
            User.objects.get(id=4),
            User.objects.get(id=3)
        )
        self.g2.followers.add(
            User.objects.get(id=5),
            User.objects.get(id=6)
        )
        self.g2.save()
