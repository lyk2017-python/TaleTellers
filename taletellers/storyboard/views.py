from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404

from storyboard.forms import ContentForm
from storyboard.models import Post


class HomeView(generic.ListView):
    def get_queryset(self):
        return Post.objects.filter(parent__isnull=True)


class StoryView(generic.CreateView):
    form_class = ContentForm
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

