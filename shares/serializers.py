from rest_framework.serializers import ModelSerializer

from shares.models import Share


class ShareSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ('time', 'user', 'liked', 'share_content_type', 'sharing_object')
