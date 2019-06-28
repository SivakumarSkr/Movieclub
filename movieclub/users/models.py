from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    contact_no = PhoneNumberField(null=True)
    place = models.CharField(max_length=20, null=True)
    followers = models.ManyToManyField('self', symmetrical=False,
                                       related_name='following')
    watched_films = models.ManyToManyField('movies.Movie', blank=True)

    # image = models.ImageField()

    def follow(self, user):
        self.followers.add(user)
        self.save()

    def unfollow(self, user):
        self.followers.remove(user)
        self.save()

    def get_followers(self):
        qs = self.followers.all()
        return qs

    def get_following(self):
        qs = self.following.all()
        return qs

    def get_number_followers(self):
        return self.followers.all().count()

    def get_number_following(self):
        return self.following.all().count()

    def get_followed_topics(self):
        return self.topics_followed.all()

    def get_drafted_blog(self):
        return self.blog_set.filter(status='D').order_by('-time')

    def get_drafted_review(self):
        return self.review_set.filter(status='D').order_by('-time')

    def get_drafted_answer(self):
        return self.answer_set.filter(status='D').order_by('-time')

    def get_published_blog(self):
        return self.blog_set.filter(status='P').order_by('-time')

    def get_published_review(self):
        return self.review_set.filter(status='P').order_by('-time')

    def get_published_answer(self):
        return self.answer_set.filter(status='P').order_by('-time')

    def get_followed_groups(self):
        return self.groups_followed.all()

    def get_watched_films(self):
        return self.watched_films.all()

    def check_watched(self, movie):
        return movie in self.watched_films.all()

    def get_followed_stars(self):
        return self.following_stars.all()

    def get_suggestions_received(self):
        return self.suggest_receiver.order_by('-time')

