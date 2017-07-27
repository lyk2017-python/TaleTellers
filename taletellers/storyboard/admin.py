from django.contrib import admin
from storyboard.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "creation_time", "parent"]
    search_fields = ["title", "content"]
    list_filter = ["creation_time", "title"]
    readonly_fields = ["creation_time"]
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
                    "parent"
                ]
            }
        )

    ]
