from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.views import View

from api.utils import (
    obj_to_post,
    prev_next_post,
)
from blog.models import (
    Post,
    Category,
    Tag,
)


class ApiPostListView(BaseListView):
    paginate_by = 3

    def get_queryset(self):
        param_cate = self.request.GET.get('category')
        param_tag = self.request.GET.get('tags')
        if param_cate:
            qs = Post.objects.filter(
                category__name__iexact=param_cate
                ).order_by('-user', '-create_dt')
        elif param_tag:
            qs = Post.objects.filter(
                tags__name__iexact=param_tag
                ).order_by('-user', '-create_dt')
        else:
            qs = Post.objects.all().order_by('-user', '-create_dt')
        return qs.select_related('category').prefetch_related('tags')

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        post_list = [obj_to_post(obj, False) for obj in qs]

        page_cnt = context['paginator'].num_pages
        cur_page = context['page_obj'].number

        json_data = {
            'postList': post_list,
            'pageCnt': page_cnt,
            'curPage': cur_page,
        }

        return JsonResponse(data=json_data, safe=True, status=200)


class ApiPostDetailView(BaseDetailView):

    def get_queryset(self):
        return Post.objects.all().order_by(
            '-user', '-create_dt').select_related(
            'category').prefetch_related('tags')

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        post = obj_to_post(obj)
        prev_post, next_post = prev_next_post(obj)

        json_data = {
            'post': post,
            'prevPost': prev_post,
            'nextPost': next_post,
        }

        return JsonResponse(data=json_data, safe=True, status=200)


class ApiCateTagListView(View):
    def get(self, request, *args, **kwargs):
        qs_cate = Category.objects.all()
        qs_tag = Tag.objects.all()

        cate_list = [cate.name for cate in qs_cate]
        tag_list = [tag.name for tag in qs_tag]

        json_data = {
            'cateList': cate_list,
            'tagList': tag_list,
        }
        return JsonResponse(data=json_data, safe=True, status=200)


class ApiPostLikeDetailView(BaseDetailView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        obj.like += 1
        obj.save()
        return JsonResponse(data=obj.like, safe=False, status=200)
