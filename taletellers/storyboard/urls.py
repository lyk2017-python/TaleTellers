from django.conf.urls import url
from storyboard.views import *

urlpatterns = [
    url(r"^$", HomeView.as_view(), name="home"),
    url(r"^sss/$", SSSView.as_view(), name="faq"),
    url(r"story/$", AddStoryFormView.as_view(), name="add_story"),
    url(r"^story/(?P<pk>\d+)/$", AddContentFormView.as_view(), name="story_detail"),
    url(r"^contact/", ContactFormView.as_view(), name="contact"),
    url(r"^register/", UserView.as_view(), name="register"),
    url(r"^top10/$", Top10View.as_view(), name="top10"),
    url(r"^ajax/user_like_response", user_like_response, name="ulr"),
    # url(r"^api/likes$", like, name="like_dislike"),     # ajax example
]
