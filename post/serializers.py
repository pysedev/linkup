from rest_framework import serializers
from post.models import Post
from tag.models import Tag
from tag.serializers import TagSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "content", "tags", "created_at", "updated_at",
                  "views_count", "comments_count", "likes_count", "post_visibility", "comment_visibility"]

        read_only_fields = (
            'id', 'user', 'tags', 'created_at', 'updated_at', 'views_count', 'comments_count', 'likes_count')
