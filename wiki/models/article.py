from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)


    @property
    def preview(self):
        return self.body[:1000]