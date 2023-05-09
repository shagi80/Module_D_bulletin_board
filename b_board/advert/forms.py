""" формы объявлений """
from django import forms
from tinymce.widgets import TinyMCE
from .models import Advert, Comment


class AdvertForm(forms.ModelForm):

    class Meta():
        model = Advert
        fields = ( 'category', 'title', 'text', 'author')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введите заголовок новости ..."}),      
            'text': TinyMCE(),
            'author': forms.HiddenInput(),
        }

    def __init__(self,  *args, author=None, **kwargs):
        """ устанавливаем автора """
        super(AdvertForm, self).__init__(*args, **kwargs)
        if author:
            self.initial['author'] = author


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ( 'text', 'author', 'advert')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'placeholder': "Введите текс комментария ..."}),      
            'author': forms.HiddenInput(),
            'advert': forms.HiddenInput(),
        }

    def __init__(self,  *args, advert=None, author=None, **kwargs):
        """ устанавливаем автора """
        super(CommentForm, self).__init__(*args, **kwargs)
        if advert:
            self.initial['advert'] = advert
        if author:
            self.initial['author'] = author