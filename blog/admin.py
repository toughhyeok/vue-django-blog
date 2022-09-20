from django.contrib import admin
from django.utils.safestring import mark_safe

from blog.models import (
    Post,
    Category,
    Tag,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'tag_list',
        'title',
        'description',
        'image',
        'image_thumbnail',
        'create_dt',
        'update_dt',
        'like',
    )

    def tag_list(self, obj):
        return ','.join([t.name for t in obj.tags.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe(
                '<img src="{url}" width="70px"/>'.format(
                    url=obj.image.url,
                ))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
