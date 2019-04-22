from django.contrib import admin
from .models import Article, Discussion, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(Discussion)
admin.site.register(Comment)