from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    """This class arranges user posts. A post might contain a title or content but it can't contain
    both. If a post has a title, that post must be parent of other posts. Content posts must be
    child of title posts."""
    title = models.CharField(max_length=100, blank=True, null=True)     # unique=True might be added
    content = models.CharField(max_length=140)
    creation_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    super_parent = models.ForeignKey("self", blank=True, null=True, related_name="super_children")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        # returns the id and the title of the Post class's objects when it's requested on manage.py's shell
        return "#{0} {1}".format(self.id, self.title)

    def can_fork(self):
        """Eger bir postun fork sayisi 3'ten kucukse true, buyukse false
        dondurur. Fork sayisini kontrol etmek icin kullaniyoruz."""
        return self.children.count() < 3

    def get_parents(self, exclude_self=False):
        """
        Herhangi bir postun bütün parentlarını içeren ve ilk posttan başlayarak sıralayan
        bir liste döndürür. Post.get_parent() ile çağırılabilir.
        """
        story = self
        story_list = []
        while story.parent is not None:
            story_list.append(story)
            story = story.parent
        else:
            story_list.append(story)
        story_list.reverse()
        if exclude_self:
            story_list.pop(-1)
        return story_list

    class Meta:
        """
        get_latest_by: ???

        unique_together: Tek başına eşsiz olmasalar da hepsi birlikte eşsiz olması gereken
        durumlar için kullanlır.
        """
        get_latest_by = "creation_time"
        unique_together = ("content", "parent")


@receiver(post_save, sender=Post)
def add_super_parent_to_first_post(sender, instance, *args, **kwargs):
    """
    Yeni hikaye eklendiğinde bu hikatenin kendi super_parent'ı olmasını sağlar.
    """
    if instance.title:
        sender.objects.filter(id=instance.id).update(super_parent=instance)


