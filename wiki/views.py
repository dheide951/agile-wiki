from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from wiki.models import Article, Discussion, Comment, Donation
from wiki.forms import ArticleForm, DiscussionForm, CommentForm
from django.views import View
from django.views.generic import DetailView, ListView
from decouple import config
from django.contrib import messages
import stripe


def index(request):
    top_articles = Article.objects.filter(rating__gt=3, completed=True)
    context = {'top_articles': top_articles}
    return render(request, 'wiki/index.html', context)


def donate(request):
    context = {'stripe_pk': config('STRIPE_PK')}
    return render(request, 'wiki/donate_form.html', context)


def accept_donation(request):
    if request.method == 'POST':
        stripe.api_key = config('STRIPE_SK')

        if not all([request.POST['amount'], request.POST['name'], request.POST['stripeToken']]):
            messages.error(request, 'Not enough information was submitted')
            redirect('donate')

        amount = int(float(request.POST['amount']) * 100)
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            source=request.POST['stripeToken'],
            description='Donation for agile wiki'
        )

        if not charge['status'] == 'succeeded':
            messages.error(request, charge['failure_message'])

        donation = Donation(
            name=request.POST['name'],
            amount=amount,
            invoice=charge['invoice']
        )
        donation.save()

        messages.success(request, 'Successfully Donated, Thank You')

        return redirect('index')

    return redirect('donate')


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

        messages.error(request, 'Something went wrong')

    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def add_article_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect('article-detail', pk=pk)
        messages.error(request, 'Something went wrong')

    return redirect('article-detail', pk=pk)


def add_discussion_comment(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.discussion = discussion
            comment.save()
            return redirect('discussion-detail', pk=pk)

        messages.error(request, 'Something went wrong')

    return redirect('discussion-detail', pk=pk)


def rate_article(request, pk):
    article = Article.objects.get(pk=pk)

    if not article:
        return redirect('articles')

    if request.method == 'POST':
        if 'rate' in request.POST:
            if request.POST['rate']:
                article.calculate_rating(request.POST['rate'])

    return redirect('article-detail', pk=pk)


def complete_article(request, pk):
    article = Article.objects.get(pk=pk)

    if not article:
        messages.error(request, 'Article does not exist')
        return redirect('articles')
    article.completed = True
    article.save()

    return redirect('article-detail', pk=article.id)


def delete_article(request, pk):
    article = Article.objects.get(pk=pk)

    if not article:
        messages.error(request, 'Article does not exist')
        return redirect('articles')

    article.delete()
    return redirect('user-articles')


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    article = comment.article

    if not comment:
        messages.error(request, 'Comment does not exist')
        return redirect('articles')

    comment.delete()
    return redirect('article-detail', pk=article.pk)


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(completed=True)


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'key': 'value'})
        return context


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
        if 'pk' in kwargs:
            if kwargs['pk']:
                article = Article.objects.get(pk=kwargs['pk'])
                if not article:
                    messages.error(request, 'Article does not exist')
                    return redirect('add-article')
                form = self.form_class(instance=article)
            return render(request, 'wiki/edit_article.html', {'form': form})

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, initial=self.initial)
        if 'pk' in kwargs:
            if kwargs['pk']:
                article = Article.objects.get(pk=kwargs['pk'])
                if not article:
                    messages.error(request, 'Article does not exist')
                    return redirect('add-article')
                form = self.form_class(request.POST, instance=article)

        if form.is_valid():

            article = form.save(commit=False)
            article.user = request.user

            if 'post' in form.data:
                article.completed = True

            article.save()

            return redirect('article-detail', pk=article.pk)

        return render(request, self.template_name, {'form': form})


class DiscussionListView(ListView):
    model = Discussion


class DiscussionDetailView(DetailView):
    model = Discussion

    def get_context_data(self, **kwargs):
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'key': 'value'})
        return context


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
