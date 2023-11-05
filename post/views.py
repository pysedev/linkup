from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from post.serializers import PostSerializer
from post.models import Post
from rest_framework.response import Response
from rest_framework import status
from utility.permissions import IsOwnerOrReadOnly
from tag.models import Tag


def set_tags(request, post):
    tag_data = request.data.get('tags')
    if tag_data:
        if tag_data.startswith("[") and tag_data.endswith("]"):
            list_tag = str(tag_data).replace("[", "").replace("]", "").split(",")
            if len(list_tag) > 0:
                post.tags.clear()
                for tag_id in list_tag:
                    try:
                        post.tags.add(Tag.objects.get(id=int(tag_id)))
                    except Tag.DoesNotExist:
                        continue


class ListCreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        info = PostSerializer(data=request.data)
        if info.is_valid():
            info.validated_data.update({'user': request.user})
            post = info.save()
            set_tags(request, post)
            return Response({"data": "post created"}, status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        info = PostSerializer(instance=Post.custom_objects.filter(user=request.user), many=True)
        return Response(info.data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroyPostView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def setup(self, request, *args, **kwargs):
        self.post = request.GET['object']
        super().setup(request, *args, **kwargs)

    def get(self, request, pk):
        info = PostSerializer(instance=self.post)
        return Response(info.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        self.check_object_permissions(request, self.post.user)
        info = PostSerializer(instance=self.post, data=request.data, partial=True)
        if info.is_valid():
            set_tags(request, self.post)
            info.save()
            return Response({"data": "post updated"}, status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.check_object_permissions(request, self.post.user)
        self.post.is_show = False
        self.post.save()
        return Response({"data": "post deleted"}, status=status.HTTP_400_BAD_REQUEST)
