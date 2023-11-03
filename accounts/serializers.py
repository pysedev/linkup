from rest_framework import serializers
from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "bio", "user"]
        extra_kwargs = {
            "id": {
                "read_only": True
            }
        }


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=6, required=True)
    verify_code = serializers.CharField(max_length=6, required=True)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return ProfileSerializer(instance=obj.user_profile).data


