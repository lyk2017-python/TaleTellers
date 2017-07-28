from django.contrib import admin
from storyboard.models import Post


class PostChildrenInLine(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "creation_time", "parent"]
    search_fields = ["title", "content"]
    list_filter = ["creation_time", "title"]
    inlines = [PostChildrenInLine]
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
                    "parent"
                ]
            }
        )
    ]
