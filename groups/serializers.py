from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit_serializer.serializers import TaggitSerializer

from groups.models import Group, GroupBlog, JoinRequest


class GroupSerializer(ModelSerializer):
    """ Serializer for Group"""
    class Meta:
        model = Group
        fields = ('uuid_id', 'name', 'time_created', 'creator', 'admins', 'type_of_group', 'description')
        read_only_fields = ('uuid_id', 'time_created', 'creator', 'admins')


class TagSerializerField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list('name', flat=True)


class GroupBlogSerializer(TaggitSerializer, ModelSerializer):
    """ Serializer for Group Blog"""

    # tags = TagListSerializerField()

    class Meta:
        model = GroupBlog
        fields = ('contents', 'image', 'heading', 'group')


class JoinRequestSerializer(ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = '__all__'
        read_only_fields = '__all__'
