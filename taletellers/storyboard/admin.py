from django.contrib import admin
from storyboard.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
