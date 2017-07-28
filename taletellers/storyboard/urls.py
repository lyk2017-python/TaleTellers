from django.conf.urls import url
from storyboard.views import *

urlpatterns = [
    url(r"^$", HomeView.as_view(), name="home"),
    url(r"^sss$", SSSView.as_view(), name="faq"),
    url(r"^story/(?P<pk>\d+)$", StoryView.as_view(), name="story_detail"),
    url(r"^contact/", ContactFormView.as_view())
    # url(r"^detay/(?P<id>\d+)-(?P<slug>[A-Za-z0-9\-]+)$", HaberView.as_view(), name="news_detail"),
]
