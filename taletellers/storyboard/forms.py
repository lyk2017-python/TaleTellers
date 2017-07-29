from django import forms
from django.forms import HiddenInput

from storyboard.models import Post


class ContentForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id", "score", "title"]
        widgets = {"parent": HiddenInput()}