from rest_framework import serializers
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['reports_count', 'management_status']
        read_only_fields = (
            'id', 'user', 'tags', 'created_at', 'updated_at', 'views_count', 'comments_count', 'likes_count')
