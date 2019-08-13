from django.contrib.auth import get_user_model
from django.test import TestCase

from comments.models import Comment
from contents.models import Blog, Status

User = get_user_model()


class CommentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user1', password='user1@user')
        User.objects.create(username='user2', password='user1@user')
        User.objects.create(username='userl', password='user2@user')
        User.objects.create(username='userd', password='user3@user')
        User.objects.create(username='usert', password='user4@user')
        User.objects.create(username='usert2', password='user4@user')
        user = User.objects.all()
        Blog.objects.create(
            user=user[0],
            status='P',
            contents='this is another begging',
            heading='just for horror',
        )
        Status.objects.create(
            user=user[1],
            action='W',
        )
        Status.objects.create(
            user=user[2],
            action='W',
        )

    def setUp(self):
        self.user = User.objects.all()
        self.status = Status.objects.all()
        self.blog = Blog.objects.all()[0]
        self.c1 = Comment.objects.create(user=self.user[3], text='good movie', content_object=self.status[0])
        self.c2 = Comment.objects.create(user=self.user[4], text='good movie', content_object=self.status[0])
        self.c3 = Comment.objects.create(user=self.user[3], text='good movie', content_object=self.status[1])
        self.c4 = Comment.objects.create(user=self.user[4], text='good movie', content_object=self.c1)
        self.c5 = Comment.objects.create(user=self.user[3], text='good movie', content_object=self.c1)

    def test_like_the_comment(self):
        self.c1.like_the_comment(self.user[1])
        self.c1.like_the_comment(self.user[0])
        self.assertEqual(self.c1.get_no_likes(), 2)
        self.c2.dislike_the_comment(self.user[1])
        self.c1.dislike_the_comment(self.user[1])
        self.assertEqual(self.c1.get_no_likes(), 1)
        self.assertEqual(self.c2.get_no_dislikes(), 1)

    def test_get_comments(self):
        self.assertEqual(self.c1.get_comments().count(), 2)


