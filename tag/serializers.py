from rest_framework import serializers
from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "description", "parent"]
        read_only_fields = ("id",)
