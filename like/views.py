from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from like.serializers import LikeSerializer
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from comment.models import Comment
from like.models import PostLike, CommentLike
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


def get_object(model, pk):
    try:
        if model == 'post':
            return Post.custom_objects.get(id=pk)
        if model == 'comment':
            return Comment.objects.get(id=pk)
    except ObjectDoesNotExist:
        return None


def is_liked(model, user, obj):
    try:
        if model == 'post':
            return PostLike.objects.get(user=user, post=obj)
        if model == 'comment':
            return CommentLike.objects.get(user=user, comment=obj)
    except ObjectDoesNotExist:
        return None


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        info = LikeSerializer(data=request.data)
        if info.is_valid():
            model = info.validated_data['model']
            obj = get_object(model, info.validated_data['id'])
            if obj:
                if model == 'post':
                    try:
                        PostLike.objects.create(user=request.user, post=obj)
                        obj.likes_count += 1
                        obj.save(update_fields=['likes_count'])
                        return Response({"data": "The post was liked"})
                    except IntegrityError:
                        PostLike.objects.get(user=request.user, post=obj).delete()
                        obj.likes_count -= 1
                        obj.save(update_fields=['likes_count'])
                        return Response({"data": "The post was disliked"})
                if model == 'comment':
                    try:
                        CommentLike.objects.create(user=request.user, comment=obj)
                        obj.likes_count += 1
                        obj.save(update_fields=['likes_count'])
                        return Response({"data": "The comment was liked"})
                    except IntegrityError:
                        CommentLike.objects.get(user=request.user, comment=obj).delete()
                        obj.likes_count -= 1
                        obj.save(update_fields=['likes_count'])
                        return Response({"data": "The comment was disliked"})
            return Response({"errors": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)


class IsLikedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        info = LikeSerializer(data=request.data)
        if info.is_valid():
            model = info.validated_data['model']
            obj = get_object(model, info.validated_data['id'])
            if obj:
                if model == 'post':
                    try:
                        PostLike.objects.get(user=request.user, post=obj)
                        return Response({"data": "The post has been liked"})
                    except ObjectDoesNotExist:
                        return Response({"data": "The post has not been liked"})
                if model == 'comment':
                    try:
                        CommentLike.objects.get(user=request.user, post=obj)
                        return Response({"data": "The comment has been liked"})
                    except ObjectDoesNotExist:
                        return Response({"data": "The comment has not been liked"})
            return Response({"errors": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
