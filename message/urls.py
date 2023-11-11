from django.urls import path
from message import views

app_name = 'message'

urlpatterns = [
    path('', views.MessageView.as_view(), name="message"),
]
