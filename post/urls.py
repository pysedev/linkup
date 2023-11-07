from django.urls import path
from like import views

app_name = 'like'

urlpatterns = [
    path('', views.LikeView.as_view(), name="like"),
]
