from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [
    path('<int:pk>/', views.RetrieveUpdateDestroyPostView.as_view(), name="detail"),
    path('', views.ListCreatePostView.as_view(), name="tag"),
]
