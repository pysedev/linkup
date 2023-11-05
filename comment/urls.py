from django.urls import path
from comment import views

app_name = 'comment'

urlpatterns = [
    path('<int:pk>/', views.RetrieveUpdateDestroyCommentView.as_view(), name="detail"),
    path('', views.ListCreateCommentView.as_view(), name="tag"),
]
