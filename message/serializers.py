from rest_framework import serializers
from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "sent_at", "is_read"]
        read_only_fields = ("id", "sender", "sent_at", "is_read")
