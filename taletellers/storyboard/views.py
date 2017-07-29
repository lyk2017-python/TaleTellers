from django.urls import reverse
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import get_object_or_404

from storyboard.forms import *
from storyboard.models import Post


class HomeView(generic.ListView):
    """
    Anasayfada skora göre sıralı ilk 5 hikayenin gösterilmesini sağlar. Ancak sadece
    birinci postun (yani başlıklı postun) skoruna bakıyor
    """
    def get_queryset(self):
        return Post.objects.filter(parent__isnull=True).order_by("-score")[:5]


class AddContentFormView(generic.CreateView):
    """
    Hikayeye içerik eklemek için gerekli olan formun sayfasının özelliklerini ayarlar.
    template_name: Hangi html dosyasını temel oalrka kullancağını belirler
    """
    form_class = AddContentForm
    template_name = "storyboard/post_detail.html"

    def get_success_url(self):
        """
        Form gönderildikten sonra hangi linke gideceğini belirler.
        Bu fonksiyonda oluşturulan yeni postun gitmesini sağlıyor
        """
        return reverse("story_detail", kwargs={"pk": self.object.id})

    def get_form_kwargs(self):
        """
        Gönder butonuna basıldığında kullanıcının gönderdiği bilgilerin
        yanında bizim de ek bilgi gönderebilmemizi sağlar. Bu fonksiyonda parent ve
        super_parent bilgilerini girerek database'de ilişki kurmamızı sağlıyor.
        """
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["parent"] = self.kwargs["pk"]
            post_data["super_parent"] = get_object_or_404(Post, id=self.kwargs["pk"]).get_parents()[0].id
            kwargs["data"] = post_data
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Bulunan posttan itibaren bütün parent'ları takip ederek en baştaki
        başlıklı posta ulaşır. Bu posta kadar olan bütün postların listesini story_list
        olarak yollar. Bu içerik daha sonra template'larda çağırılacak olan değişkenin
        ismidir.
        """
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Post, id=self.kwargs["pk"])
        context["story_list"] = context["object"].get_parents()
        return context


class AddStoryFormView(generic.CreateView):
    """
    Yeni hikaye oluşturmak için gerekli olan form sayfasının özelliklerini ayarlar.
    """
    form_class = AddStoryForm
    template_name = "storyboard/post_add.html"

    def get_context_data(self, **kwargs):
        """
        Bütün hikaye listesini alıp bunu context'e post_list olarak ekler. Böylece
        template üzerinden bu isimle çekip işlem yapabilriz.
        """
        context = super().get_context_data(**kwargs)
        context["post_list"] = list(Post.objects.filter(parent__isnull=True))
        return context


class SSSView(generic.TemplateView):
    """
    Düz sayfa içinde sadece içerik verilirken bu şekilde kullanılır. Burada
    sık sorulan sorulara link sağlıyoruz.
    """
    template_name = "storyboard/sss.html"


class ContactFormView(generic.FormView):
    """
    İletişim formu sayfası için gerekli olan özellikleri ayarlar.
    """
    form_class = ContactForm
    template_name = "storyboard/contact.html"
    success_url = "/"

    def form_valid(self, form):
        """
        Bir form gönderilirken çeşitli kontrollerden geçmesini istediğimizde kullanulan
        fonksiyondur. İçerisindeki cleaned_data ile alınan bilginin düzenlenmesini ve
        kontrol edilmesini sağlar.

        send_mail() fonksiyonu gönderilecek olan epostanın hangi formatta olacağını düzenlemek
        için kullanlır. 3 tane arguman alır. Bunlar içeriğin nasıl gözükeceğini içeren bir
        taslak, gönderiyi yapacak email, ve gönderilecek email listesi (! Liste olarak göndermeyi
        unutmuyoruz!).
        """
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
