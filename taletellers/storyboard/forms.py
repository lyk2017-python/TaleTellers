from django import forms
from django.forms import HiddenInput

from storyboard.models import Post


class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":2}))


class StoryAddForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=140)
    parent = forms.HiddenInput()
