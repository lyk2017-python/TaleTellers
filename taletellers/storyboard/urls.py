from django.conf.urls import url
from storyboard.views import HomeView, SSSView

urlpatterns = [
    url(r"^$", HomeView.as_view(), name="home"),
    url(r"^sss$", SSSView.as_view(), name="faq"),
    # url(r"^kategori/(?P<slug>[\A-Za-z0-9\-]+)/(?P<id>\d+)$", KategoriView.as_view(), name="category_detail"),
    # url(r"^detay/(?P<id>\d+)-(?P<slug>[A-Za-z0-9\-]+)$", HaberView.as_view(), name="news_detail"),
]
