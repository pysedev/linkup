from django.db import models
from django.conf import settings
from utility.choices import ACCESS_VISIBILITY, MANAGEMENT_STATUS
from tag.models import Tag


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(management_status='A', is_show=True)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    reports_count = models.PositiveIntegerField(default=0)
    post_visibility = models.CharField(max_length=2, choices=ACCESS_VISIBILITY, default='PU')
    comment_visibility = models.CharField(max_length=2, choices=ACCESS_VISIBILITY, default='PU')
    management_status = models.CharField(max_length=1, choices=MANAGEMENT_STATUS, default='A')
    is_show = models.BooleanField(default=True)
    objects = models.Manager()
    custom_objects = PostManager()

    def __str__(self) -> str:
        return self.content[:20]

    class Meta:
        default_manager_name = 'objects'
        default_related_name = 'posts'
