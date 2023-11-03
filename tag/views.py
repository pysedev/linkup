from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from tag.models import Tag
from tag.serializers import TagSerializer
from tag.permissions import IsAdminOrReadOnly


class RetrieveUpdateDestroyTagView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ListTagView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
