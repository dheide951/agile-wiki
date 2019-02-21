from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE, null=True)
    discussion = models.ForeignKey('Discussion', on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=150)