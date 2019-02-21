from django.db import models
from django.contrib.auth.models import User
from .comment import Comment


class Discussion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    @property
    def preview(self):
        return self.body[:300] + '....'

    @property
    def has_comments(self):
        return True if Comment.objects.filter(discussion=self) else False

    @property
    def reversed_comments(self):
        return self.comment_set.order_by('-id')
