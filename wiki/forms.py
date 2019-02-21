from django import forms
from wiki.models import Article


class ArticleForm(forms.ModelForm):

    title = forms.CharField(label='Title', max_length=150)
    body = forms.CharField(widget=forms.Textarea, max_length=1000)

    class Meta:
        model = Article
        fields = ['title', 'body']
