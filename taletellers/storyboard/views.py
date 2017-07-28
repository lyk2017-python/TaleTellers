from django.http import Http404
from django.views import generic
from storyboard.forms import ContentForm, ContactForm
from django.shortcuts import render

from storyboard.models import Post
from django.core.mail import send_mail


class HomeView(generic.ListView):
    def get_queryset(self):
        return Post.objects.filter(parent__isnull=True)


class StoryView(generic.CreateView):
    form_class = ContentForm
    template_name = "storyboard/post_detail.html"
    success_url = "."



"""
class StoryView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story = context["object"]
        story_list = []
        while story.parent is not None:
            story_list.append(story)
            story = story.parent
        else:
            story_list.append(story)
        story_list.reverse()
        context["story_list"] = story_list
        return context
"""


class ContactFormView(generic.FormView):
    form_class = ContactForm
    template_name = "storyboard/contact.html"
    success_url = "/"

    def form_valid(self, form):
        data = form.cleaned_data
        from django.conf import settings
        send_mail(
            "TaleTellers ContactForm : {}".format(data["title"]),
            ("Bir bildiriminiz var\n"
             "---\n"
             "{}\n"
             "---\n"
             "email={}\n"
             "ip={}").format(data["message"], data["email"], self.request.META["REMOTE_ADDR"]),
            settings.DEFAULT_FROM_EMAIL,
            ["busra@taletellers.com"]
        )
        return super().form_valid(form)


class SSSView(generic.TemplateView):
    template_name = "storyboard/sss.html"

"""
class KategoriView(generic.DetailView):
    def get_queryset(self):
        return Category.objects.all()
        

class DetayView(generic.DetayView):
    def get_queryset(self):
        return Category.objects.filter(report_count=0)
        
"""

