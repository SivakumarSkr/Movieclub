from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit_serializer.serializers import TaggitSerializer

from groups.models import Group, GroupBlog, JoinRequest, ClosedGroup


class GroupSerializer(ModelSerializer):
    """ Serializer for Group"""

    class Meta:
        model = Group
        fields = ('uuid_id', 'name', 'time_created', 'type_of_group', 'creator', 'description')
        read_only_fields = ('uuid_id', 'time_created', 'creator', 'type_of_group')


class ClosedGroupSerializer(ModelSerializer):
    class Meta:
        model = ClosedGroup
        fields = ('uuid_id', 'name', 'time_created', 'type_of_group', 'creator', 'admins', 'description')
        read_only_fields = ('uuid_id', 'time_created', 'creator', 'type_of_group', 'admins')


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
        read_only_fields = ('uuid_id', 'group', 'user', 'authorizer', 'requested_time', '')
