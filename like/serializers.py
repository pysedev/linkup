from rest_framework import serializers
from like.models import PostLike, CommentLike
from like.models import BaseLike


class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    model = serializers.ChoiceField(choices=['post', 'comment'])


