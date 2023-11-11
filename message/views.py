from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from message.models import Message
from message.serializers import MessageSerializer
from accounts.models import User


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        data = MessageSerializer(instance=messages, many=True).data
        return Response({"data": data}, status=status.HTTP_200_OK)

    def post(self, request):
        info = MessageSerializer(data=request.data)
        if info.is_valid():
            Message.objects.create(sender=request.user, receiver=info.validated_data['receiver'],
                                   content=info.validated_data['content'])
            return Response({"data": "the message sent"}, status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
