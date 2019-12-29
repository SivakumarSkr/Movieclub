from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from comments.models import Comment
from contents.models import Answer, Blog, Review, Status
from groups.models import GroupBlog
from notifications.models import Notification
from shares.models import Share
from suggestions.models import Suggestion

User = get_user_model()


@receiver(signal=signals.post_save, sender=Suggestion)
def suggest_notification(sender, instance, created, **kwargs):
    if created:
        data = {
            "creator": instance.sender,
            "receiver": instance.receiver,
            "category": "SG",
            "subject_object": instance
        }
        notification_object = Notification(**data)
        notification_object.save()


@receiver(signals.post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        data = {
            "creator": instance.user,
            "subject_object": instance,
            "receiver": instance.content_obj.user
        }
        content_obj = instance.content_object
        if isinstance(content_obj, sender):
            data["category"] = "RP"
        else:
            data["category"] = 'CM'
        notification_object = Notification(**data)
        notification_object.save()


@receiver(signals.m2m_changed, sender=User.followers.through)
def following_user_notification(sender, **kwargs):
    action = kwargs.pop('action', None)
    instance = kwargs.pop('instance', None)
    pk_set = list(kwargs.pop('pk_set', None))
    follower = User.objects.get(pk=pk_set[0])
    if action == 'post_add':
        data = {
            "creator": follower,
            "receiver": instance,
            "subject_object": instance,
            "category": "FL"
        }
        notification_object = Notification(**data)
        notification_object.save()


@receiver(signals.post_save, sender=Share)
def share_notification(sender, instance, created, **kwargs):
    if created:
        data = {
            "creator": instance.user,
            "receiver": instance.content_obj.user,
            "subject_object": instance,
            "category": "SR"
        }
        notification_object = Notification(**data)
        notification_object.save()


@receiver(signals.post_save, sender=Answer)
def answer_notification(sender, instance, created, **kwargs):
    if created:
        data = {
            "creator": instance.user,
            "receiver": instance.topic.created_by,
            "subject_object": instance,
            "category": 'AN'
        }
        notification_object = Notification(**data)
        notification_object.save()


def like_notification(model):
    # function for creating signals of Answer, Blog, Review

    @receiver(signals.m2m_changed, sender=model.liked.through)
    def like(sender, **kwargs):
        action = kwargs.pop('action', None)
        instance = kwargs.pop('instance', None)
        pk_set = list(kwargs.pop('pk_set', None))
        creator = User.objects.get(pk=pk_set[0])
        if action == 'post_add' and creator != instance.user:
            data = {
                'creator': creator,
                'receiver': instance.user,
                'subject_object': instance,
                'category': 'LK'
            }
            notification_object = Notification(**data)
            notification_object.save()

    return like


like_the_answer = like_notification(Answer)
like_the_blog = like_notification(Blog)
like_the_review = like_notification(Review)
like_the_status = like_notification(Status)
like_the_group_blog = like_notification(GroupBlog)
