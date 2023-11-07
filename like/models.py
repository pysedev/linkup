from django.db import models
from django.conf import settings
from post.models import Post
from comment.models import Comment


class BaseLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PostLike(BaseLike):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["user", "post"]]


class CommentLike(BaseLike):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["user", "comment"]]
