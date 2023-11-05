from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('tag/', include('tag.urls', namespace='tag')),
    path('post/', include('post.urls', namespace='post')),


]
