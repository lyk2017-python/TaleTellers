from django import forms
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
            "super_parent": HiddenInput()
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
            "super_parent": HiddenInput()
        }


class UserForm(forms.ModelForm):
    """
    Yeni kullanici olusturmak icin kullanilan form
    """
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        exclude = [
            "id",
            "last_login",
            "date_joined",
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
            "is_active",
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }

