from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "slug", "author",)
    prepopulated_fields = {
        "slug": ("title",),
    }

# @admin.register(models.Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("post", "id", "name", "email", "publish", "status")
#     list_filter = ("status", "publish")
#     search_fields = ("name", "email", "content")


admin.site.register(models.Category)

admin.site.register(models.Comment, MPTTModelAdmin)

