from django import forms


class NewsForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    text = forms.CharField(label='text', max_length=1000)


class SearchForm(forms.Form):
    q = forms.CharField(label='q', max_length=100)
