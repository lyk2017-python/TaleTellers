from django.contrib import admin
from storyboard.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Admin ana panelinde görünecek olan sütunları belirler
    list_display = ["title", "content", "score", "creation_time", "super_parent"]
    search_fields = ["title", "content", "super_parent"]
    # Hangi listeler ile gruplamaya izin verileceğini seçmek için
    list_filter = ["creation_time", ("super_parent", admin.RelatedOnlyFieldListFilter)]
    # Değiştirlmesini istemediğimiz bölümler
    readonly_fields = ["creation_time", "parents", "super_parent"]
    fieldsets = [
        (
            "Globals", {
                "fields": [
                    "title",
                    "content",
                    "parent"
                ]
            }
        ),
        (
            "Others", {
                "fields": [
                    "score",
                    "creation_time",
                    "parents",
                    "super_parent"
                ]
            }
        )

    ]

    def parents(self, object):
        """
        Bakmak istediğimiz postun bağlı olduğu hikaye ağacını listeler.
        Böyle bir fonksiyon ile yeni bir kategori tanımlamak mümkün olur.
        """
        parents = object.get_parents(exclude_self=True)
        if parents:
            return "<br>".join([obj.content for obj in parents])
        else:
            return ""
    parents.allow_tags = True
