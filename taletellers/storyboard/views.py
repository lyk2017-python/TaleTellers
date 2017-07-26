from django.views import generic
from django.shortcuts import render

from storyboard.models import Post


class HomeView(generic.ListView):
    def get_queryset(self):
        return Post.objects.filter(parent=None)


class StoryView(generic.ListView):
    pass


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

