from django import forms
from django.forms import HiddenInput

from storyboard.models import Post


class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":2}))