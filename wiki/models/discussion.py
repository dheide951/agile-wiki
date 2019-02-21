from django.db import models
from django.contrib.auth.models import User


class Discussion(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def preview(self):
        return self.body[:300] + '....'
