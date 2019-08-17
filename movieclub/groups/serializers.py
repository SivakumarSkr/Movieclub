from rest_framework.serializers import ModelSerializer

from groups.models import Group, GroupBlog


class GroupSerializer(ModelSerializer):
    """ Serializer for Group"""
    class Meta:
        model = Group
        fields = ('name', 'time_created', 'creator', 'admins', 'type_of_group', 'description', )


class GroupBlogSerializer(ModelSerializer):
    """ Serializer for Group Blog"""
    class Meta:
        model = GroupBlog
        fields = ('tags', 'contents', 'image', 'heading')