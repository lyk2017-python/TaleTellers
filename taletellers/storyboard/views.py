from django.conf.global_settings import AUTH_USER_MODEL as User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import get_object_or_404


from storyboard.forms import *
from storyboard.models import Post


class HomeView(generic.ListView):
    """
    Anasayfada skora göre sıralı ilk 5 hikayenin gösterilmesini sağlar. Ancak sadece
    birinci postun (yani başlıklı postun) skoruna bakıyor
    """
    template_name = "storyboard/post_list.html"
    paginate_by = 5

    def get_queryset(self):
        post_list = []
        if Post.objects.all():
            for i in Post.objects.filter(parent__isnull=True):
                children = Post.objects.filter(super_parent=i).latest()
                post_list.append(children.id)
            post_list = [(i.super_parent, i.creation_time) for i in Post.objects.filter(id__in=post_list).order_by("-creation_time")]
        else:
            post_list = []
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_users = []
        for i in User.objects.all():
            top_users.append((i,  i.post.all().aggregate(Sum("score"))["score__sum"]))
        context["top_users"] = sorted(top_users, key=lambda x: x[1], reverse=True)
        return context


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
            post_data["author"] = self.request.user.id
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
        context["top"] = Post.objects.filter(super_parent=context["story_list"][0]).order_by("-score")[0]
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, id=self.kwargs["pk"])
        if obj.can_fork():
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("<h1>403 FORBIDDEN</h1>")


class AddStoryFormView(LoginRequiredMixin, generic.CreateView):
    """
    Yeni hikaye oluşturmak için gerekli olan form sayfasının özelliklerini ayarlar.
    """
    form_class = AddStoryForm
    template_name = "storyboard/post_add.html"
    success_url = "."

    def get_form_kwargs(self):
        """
        Gönder butonuna basıldığında kullanıcının gönderdiği bilgilerin
        yanında bizim de ek bilgi gönderebilmemizi sağlar. Bu fonksiyonda parent ve
        super_parent bilgilerini girerek database'de ilişki kurmamızı sağlıyor.
        """
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["author"] = self.request.user.id
            kwargs["data"] = post_data
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Bütün hikaye listesini alıp bunu context'e post_list olarak ekler. Böylece
        template üzerinden bu isimle çekip işlem yapabilriz.
        """
        context = super().get_context_data(**kwargs)
        context["post_list"] = list(Post.objects.filter(parent__isnull=True))
        return context


class UserView(generic.CreateView):
    """
    Yeni kullanici olusturmak icin gerekli olan form sayfasinin ozelliklerini ayarlar.
    """
    form_class = UserForm
    template_name = "storyboard/register.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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


class Top10View(generic.ListView):
    template_name = "storyboard/top10_list.html"
    paginate_by = 10

    def get_queryset(self):
        score_list = dict()
        if Post.objects.all():
            for i in Post.objects.filter(parent__isnull=True):
                children = Post.objects.filter(super_parent=i).aggregate(Sum("score"))
                score_list[i] = children["score__sum"]
                sorted_score_list = sorted(score_list.items(), key=lambda x: x[1], reverse=True)
        else:
            sorted_score_list = []
        return [(i+1, e, f) for i, (e, f) in enumerate(sorted_score_list)]


def user_like_response(request):
    id = request.GET.get("id", None)
    data = {
        "score": Post.objects.filter(id=id)[0].score
    }
    return JsonResponse(data)


def like(request):
    id = request.GET.get("id", default=None)
    like = request.GET.get("like")
    obj = get_object_or_404(Post, id=int(id))
    if like == "true":
        # f objesi veri tabanindaki ilgili sutunun degerini cekerek
        # atama yapmak yerine arttirma veya azaltma yapmamizi saglar.
        obj.score = F("score") + 1
        obj.save(update_fields=["score"])
    elif like == "false":
        obj.score = F("score") - 1
        obj.save(update_fields=["score"])
    else:
        return HttpResponse(status=400)
    obj.refresh_from_db()
    return JsonResponse({"like": obj.score, "id": id})



