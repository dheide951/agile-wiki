from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from wiki.models import Article, Discussion
from wiki.forms import ArticleForm, DiscussionForm
from django.views import View
from django.views.generic import DetailView, ListView


def index(request):
    return render(request, 'wiki/index.html')


def register(request):
    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')

    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article


class UserArticleView(ListView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


class ArticleFormView(View):
    form_class = ArticleForm
    initial = {'key': 'value'}
    template_name = 'wiki/add_article.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('article-detail', pk=article.pk)

        return render(request, self.template_name, {'form': form})


class DiscussionListView(ListView):
    model = Discussion


class DiscussionDetailView(DetailView):
    model = Discussion


class UserDiscussionView(ListView):
    model = Discussion

    def get_queryset(self):
        return Discussion.objects.filter(user=self.request.user)


class DiscussionFormView(View):
    form_class = DiscussionForm
    initial = {'key': 'value'}
    template_name = 'wiki/add_discussion.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.user = request.user
            discussion.save()
            return redirect('discussion-detail', pk=discussion.pk)

        return render(request, self.template_name, {'form': form})
