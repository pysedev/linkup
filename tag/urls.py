from django.urls import path
from tag.views import ListTagView, RetrieveUpdateDestroyTagView

app_name = 'tag'

urlpatterns = [
    path('detail/<int:pk>/', RetrieveUpdateDestroyTagView.as_view(), name="detail"),
    path('', ListTagView.as_view(), name="tag"),
]
