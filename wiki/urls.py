from django.urls import path
from .views import (
    ArticleFormView,
    ArticleListView,
    ArticleDetailView,
    UserArticleView,
    DiscussionFormView,
    DiscussionListView,
    DiscussionDetailView,
    UserDiscussionView
)
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add-article/', login_required(ArticleFormView.as_view()), name='add-article'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('user/articles/', login_required(UserArticleView.as_view()), name='user-articles'),
    path('add-discussion/', login_required(DiscussionFormView.as_view()), name='add-discussion'),
    path('discussions/', DiscussionListView.as_view(), name='discussions'),
    path('discussions/<int:pk>', DiscussionDetailView.as_view(), name='discussion-detail'),
    path('user/discussions/', login_required(UserDiscussionView.as_view()), name='user-discussion'),
    path('articles/<int:pk>/comment', login_required(views.add_article_comment), name='article-comment'),
    path('discussions/<int:pk>/comment', login_required(views.add_discussion_comment), name='discussion-comment'),
    path('articles/<int:pk>/rate', login_required(views.rate_article), name='rate')
]
