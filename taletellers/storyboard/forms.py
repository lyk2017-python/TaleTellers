from django import forms
from django.forms import HiddenInput

from storyboard.models import Post


class ContentForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = [
            "id",
            "score",
            "parent",
        ]
        widgets = {
            "categories": HiddenInput()
        }


class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}))
    ip = forms.GenericIPAddressField(widget=forms.HiddenInput())