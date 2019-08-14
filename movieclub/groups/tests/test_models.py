from django.test import TestCase

from users.models import User

from groups.models import Group, GroupBlog


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
        self.user = User.objects.all()
        self.g1 = Group.objects.create(
            name='korean lovers',
            description='something',
            creator=self.user[0]
        )
        self.g2 = Group.objects.create(
            name='korean lovers',
            description='something',
            type_of_group='C',
            creator=self.user[1],
        )
        self.g3 = Group.objects.create(
            name='korean lovers',
            description='something',
            creator=self.user[2],
        )
        self.gb1 = GroupBlog.objects.create(
            user=self.user[4],
            contents='just something',
            heading='heading',
            group=self.g1,
        )
        self.gb2 = GroupBlog.objects.create(
            user=self.user[5],
            contents='just something',
            heading='heading',
            group=self.g1,
        )

    def test_following_group(self):
        self.g1.follow(self.user[1])
        self.g1.follow(self.user[3])
        self.assertEqual(self.g1.check_following(self.user[2]), False)
        self.assertEqual(self.g1.check_following(self.user[1]), True)
        self.assertEqual(self.g1.get_followers().count(), 2)
        self.assertEqual(self.g2.get_followers().count(), 0)
        self.g1.un_follow(self.user[3])
        self.assertEqual(self.g1.get_followers().count(), 1)

    def test_admins(self):
        self.g2.add_admin(self.user[3])
        self.g2.add_admin(self.user[4])
        self.assertEqual(self.g2.get_admins().count(), 2)

    def test_check_closed(self):
        self.assertEqual(self.g2.check_closed(), True)
        self.assertEqual(self.g1.check_closed(), False)

    def test_check_string(self):
        self.assertEqual(str(self.g1), 'korean lovers')

    def test_group_blog(self):
        self.assertEqual(self.g1.get_group_blog().count(), 2)

    def test_blog_heading(self):
        self.assertEqual(str(self.gb1), 'heading')




