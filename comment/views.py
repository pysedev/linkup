from rest_framework.response import Response
from rest_framework.views import APIView
from comment.serializers import CommentSerializer
from utility.permissions import IsOwnerOrReadOnly
from rest_framework import status
from comment.models import Comment


class RetrieveUpdateDestroyCommentView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def setup(self, request, *args, **kwargs):
        self.comment = request.GET['object']
        super().setup(request, *args, **kwargs)

    def get(self, request, pk):
        info = CommentSerializer(instance=self.comment)
        return Response(info.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        self.check_object_permissions(request, self.comment.user)
        info = CommentSerializer(instance=self.comment, data=request.data, partial=True)
        if info.is_valid():
            if info.validated_data.get('post'):
                del info.validated_data['post']
            info.save()
            return Response({"data": "comment updated"}, status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.check_object_permissions(request, self.comment.user)
        self.comment.delete()
        return Response({"data": "comment deleted"}, status=status.HTTP_400_BAD_REQUEST)


class ListCreateCommentView(APIView):

    def get(self, request):
        info = CommentSerializer(instance=Comment.objects.filter(user=request.user), many=True)
        return Response(info.data, status=status.HTTP_200_OK)

    def post(self, request):
        info = CommentSerializer(data=request.data)
        if info.is_valid():
            info.validated_data.update({'user': request.user})
            info.save()
            return Response({"data": "comment created"}, status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
