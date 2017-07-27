from django.contrib import admin
from storyboard.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "creation_time", "parent"]
    search_fields = ["title", "content"]
    list_filter = ["creation_time", "title"]
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
