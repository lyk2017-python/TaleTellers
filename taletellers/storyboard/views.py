from django.urls import reverse
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import render, get_object_or_404

from storyboard.forms import *
from storyboard.models import Post


class HomeView(generic.ListView):
    def get_queryset(self):
        return Post.objects.filter(parent__isnull=True).order_by("-score")


class AddContentFormView(generic.CreateView):
    form_class = AddContentForm
    template_name = "storyboard/post_detail.html"

    def get_success_url(self):
        return reverse("story_detail", kwargs={"pk": self.object.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["parent"] = self.kwargs["pk"]
            kwargs["data"] = post_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Post, id=self.kwargs["pk"])
        context["story_list"] = context["object"].get_parents()
        return context


class AddStoryFormView(generic.CreateView):
    form_class = AddStoryForm
    template_name = "storyboard/post_add.html"

    def get_success_url(self):
        return reverse("add_story")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = list(Post.objects.filter(parent__isnull=True))
        return context


class SSSView(generic.TemplateView):
    template_name = "storyboard/sss.html"


class ContactFormView(generic.FormView):
    form_class = ContactForm
    template_name = "storyboard/contact.html"
    success_url = "/"

    def form_valid(self, form):
        data = form.cleaned_data
        from django.conf import settings
        send_mail(
            "HikayeKitabi ContactForm: {}".format(data["title"]),
            ("Sistemimizde harika\n"
             "---\n"
             "{}\n"
             "---\n"
             "eposta={}\n"
             "ip={}").format(data["body"], data["email"], self.request.META["REMOTE_ADDR"]),
            settings.DEFAULT_FROM_EMAIL,
            ["bilal@taletellers.com"]
        )
        return super().form_valid(form)
