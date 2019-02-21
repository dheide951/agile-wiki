from django.urls import path
from .views import ArticleFormView, ArticleListView, ArticleDetailView, UserArticleView
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add-article/', login_required(ArticleFormView.as_view()), name='add-article'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>', ArticleDetailView.as_view(), name='detail'),
    path('user/articles/', login_required(UserArticleView.as_view()), name='user-articles')
]