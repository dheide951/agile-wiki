from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from .comment import Comment


class Article(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    rate_count = models.IntegerField(default=0)
    rate_total = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    @property
    def preview(self):
        return self.body[:500] + '...'

    @property
    def has_comments(self):
        return True if Comment.objects.filter(article=self) else False

    @property
    def reversed_comments(self):
        return self.comment_set.order_by('-id')

    def calculate_rating(self, rating):
        self.rate_count += 1
        self.rate_total += int(rating)
        self.rating = round(self.rate_total / self.rate_count)
        self.save()


