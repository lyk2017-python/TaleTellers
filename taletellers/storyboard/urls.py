from django.conf.urls import url
from storyboard.views import HomeView

urlpatterns = [
    url(r"^$", HomeView, name="home"),
    # url(r"^kategori/(?P<slug>[\A-Za-z0-9\-]+)/(?P<id>\d+)$", KategoriView, name="category_detail"),
    # url(r"^detay/(?P<id>\d+)-(?P<slug>[A-Za-z0-9\-]+)$", HaberView, name="news_detail"),
    # url(r"^sss$", SSSView, name="faq"),
]
