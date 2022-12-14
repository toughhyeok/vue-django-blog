from django.contrib import (
    admin,
    messages
)
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.utils.safestring import mark_safe

from blog.models import (
    Post,
    Category,
    Tag,
    UserName
)

from job import create_crawlers


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'user',
        'tag_list',
        'title',
        'description',
        'original_url',
        'image',
        'image_thumbnail',
        'create_dt',
        'update_dt',
        'like',
    )

    actions = ['SHARE_BLOG_get_the_latest_blog_posts',
               'MEVN_STUDY_get_the_latest_blog_posts']

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST \
                and (request.POST['action'] ==
                     'SHARE_BLOG_get_the_latest_blog_posts'
                     or request.POST['action'] ==
                     'MEVN_STUDY_get_the_latest_blog_posts'):
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Post.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(PostAdmin, self).changelist_view(request, extra_context)

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

    def original_url(self, obj):
        if obj.url:
            return mark_safe(
                '<a href={url}>{url}</a>'.format(
                    url=obj.url,
                )
            )

    def SHARE_BLOG_get_the_latest_blog_posts(self, request, queryset):
        cnt = len(queryset)
        crawlers = create_crawlers("share-blog")
        for c in crawlers:
            c.crawl()
        cnt = Post.objects.all().count() - cnt
        if cnt:
            msg = '{} posts were created successfully.'.format(cnt)
        else:
            msg = 'It is already up to date.'
        self.message_user(request, msg, messages.SUCCESS)

    def MEVN_STUDY_get_the_latest_blog_posts(self, request, queryset):
        cnt = len(queryset)
        crawlers = create_crawlers("mevn-study")
        for c in crawlers:
            c.crawl()
        cnt = Post.objects.all().count() - cnt
        if cnt:
            msg = '{} posts were created successfully.'.format(cnt)
        else:
            msg = 'It is already up to date.'
        self.message_user(request, msg, messages.SUCCESS)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(UserName)
class UserName(admin.ModelAdmin):
    list_display = ('id', 'name')
