from django import forms
from django.forms import HiddenInput

from storyboard.models import Post


class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":2}))


class ContentForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id", "score", "title"]
        widgets = {"parent": HiddenInput()}


class StoryForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id", "score", "parent"]