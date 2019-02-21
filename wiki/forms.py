from django import forms
from wiki.models import Article, Discussion


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=150)
    body = forms.CharField(widget=forms.Textarea, max_length=5000)

    class Meta:
        model = Article
        fields = ['title', 'body']


class DiscussionForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=150)
    body = forms.CharField(widget=forms.Textarea, max_length=2000)

    class Meta:
        model = Discussion
        fields = ['title', 'body']
