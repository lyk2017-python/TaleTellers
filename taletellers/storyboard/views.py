from django.views import generic
from django.shortcuts import render

from storyboard.models import Post


class HomeView(generic.ListView):
    model = Post
    # def get_queryset(self):
    #     return Post.objects.filter(parent=False)


class StoryView(generic.ListView):
    pass

"""
class KategoriView(generic.DetailView):
    def get_queryset(self):
        return Category.objects.all()
        

class DetayView(generic.DetayView):
    def get_queryset(self):
        return Category.objects.filter(report_count=0)
        
        
class SSSView(generic.TemplateView):
    template_name = "blog/sss.html"

"""
