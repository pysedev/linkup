from django.urls import path
from like import views

app_name = 'like'

urlpatterns = [
    path('', views.LikeView.as_view(), name="like"),
    path('is/', views.IsLikedView.as_view(), name="is_like"),
]
