from django.views import generic
from django.shortcuts import render

from storyboard.models import Post


class HomeView(generic.ListView):
    def get_queryset(self):
        return Post.objects.filter(parent__isnull=True)


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

