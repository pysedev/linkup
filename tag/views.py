from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utility.permissions import IsAdminOrReadOnly
from tag.serializers import TagSerializer
from tag.models import Tag


class RetrieveUpdateDestroyTagView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def setup(self, request, *args, **kwargs):
        self.tag = request.GET['object']
        super().setup(request, *args, **kwargs)

    def get(self, request, pk):
        info = TagSerializer(instance=self.tag)
        return Response(info.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        info = TagSerializer(instance=self.tag, data=request.data, partial=True)
        if info.is_valid():
            info.save()
            return Response({"data": "tag updated"}, status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.tag.delete()
        return Response({"data": "tag deleted"}, status=status.HTTP_400_BAD_REQUEST)


class ListTagView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request):
        info = TagSerializer(data=request.data)
        if info.is_valid():
            info.save()
            return Response({"data": "tag created"}, status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        info = TagSerializer(instance=Tag.objects.all(), many=True)
        return Response(info.data, status=status.HTTP_200_OK)
