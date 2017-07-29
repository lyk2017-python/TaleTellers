from django.contrib import admin
from storyboard.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "creation_time", "parent"]
    search_fields = ["title", "content"]
    list_filter = ["creation_time", "title"]
    readonly_fields = ["creation_time", "parents"]
    fieldsets = [
        (
            "Globals", {
                "fields": [
                    "title",
                    "content"
                ]
            }
        ),
        (
            "Others", {
                "fields": [
                    "score",
                    "creation_time",
                    "parent",
                    "parents"
                ]
            }
        )

    ]

    def parents(self, object):
        parents = object.get_parents(exclude_self=True)
        if parents:
            return "<br>".join([obj.content for obj in parents])
        else:
            return ""
    parents.allow_tags = True