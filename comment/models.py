from django.db import models
from django.conf import settings
from post.models import Post
from utility.choices import MANAGEMENT_STATUS


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    published_at = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    management_status = models.CharField(max_length=1, choices=MANAGEMENT_STATUS, default='A')
    likes_count = models.PositiveIntegerField(default=0)
    reports_count = models.PositiveIntegerField(default=0)

    class Meta:
        default_related_name = 'comments'
