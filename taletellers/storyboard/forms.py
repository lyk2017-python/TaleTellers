from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import HiddenInput

from storyboard.models import Post
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    """
    İletişim Formu: email, başlık ve içerik alarak bunu postlamaya yarar
    """
    email = forms.EmailField()
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}))


class AddContentForm(forms.ModelForm):
    """
    Olan hikayenin devamını yazabilmek için kullanılan form
    """
    class Meta:
        model = Post
        exclude = ["id", "score", "title"]
        widgets = {
            "parent": HiddenInput(),
            "super_parent": HiddenInput(),
            "author": HiddenInput()
        }


class AddStoryForm(forms.ModelForm):
    """
    Yeni hikaye oluşturmak için kulanılan form
    """
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}))

    class Meta:
        model = Post
        exclude = ["id", "score", "parent"]
        widgets = {
            "super_parent": HiddenInput(),
            "author": HiddenInput()
        }


class UserForm(UserCreationForm):
    """
    Yeni kullanici olusturmak icin kullanilan form
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

