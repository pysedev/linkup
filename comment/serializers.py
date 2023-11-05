from rest_framework import serializers
from comment.models import Comment
from post.serializers import PostSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['reports_count', 'management_status']
        read_only_fields = ('id', 'user', 'published_at', 'likes_count')
