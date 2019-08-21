from django.contrib.auth import get_user_model
from django.test import TestCase
# from users.models import User
from contents.models import Blog
from comments.models import Comment
from shares.models import Share

User = get_user_model()


class ShareTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='user1@gmail.com', password='user2')
        User.objects.create(email='user2@gmail.com', password='user2')
        User.objects.create(email='user3@gmail.com', password='user2')
        User.objects.create(email='user4@gmail.com', password='user2')
        User.objects.create(email='user5@gmail.com', password='user2')
        User.objects.create(email='user6@gmail.com', password='user2')
        users = User.objects.all()
        Blog.objects.create(
            user=users[0],
            status='P',
            heading="something just like this",
        )

    def setUp(self):
        self.users = User.objects.all()
        self.share1 = Share.objects.create(
            user=self.users[3],
            sharing_object=Blog.objects.all()[0],
        )
        self.share2 = Share.objects.create(
            user=self.users[3],
            sharing_object=Blog.objects.all()[0],
        )
        Comment.objects.create(
            user=self.users[1],
            text='just something',
            content_object=self.share1,
        )
        Comment.objects.create(
            user=self.users[1],
            text='just something',
            content_object=self.share1,
        )
        Comment.objects.create(
            user=self.users[2],
            text='just something',
            content_object=self.share2,
        )

    def test_like_the_share(self):
        self.share1.like_the_share(self.users[5])
        self.share1.like_the_share(self.users[4])
        self.assertEqual(self.share1.liked.all().count(), 2)

    def test_get_comments(self):
        a = self.share1.get_comments()
        self.assertEqual(a.count(), 2)
        b = self.share2.get_comments()
        self.assertEqual(b.count(), 1)
