from django.http import JsonResponse
from django.views.generic.edit import BaseCreateView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.views import View

from api.utils import (
    obj_to_post,
    obj_to_comment,
    prev_next_post,
)
from blog.models import (
    Comment,
    Post,
    Category,
    Tag,
)


class ApiPostListView(BaseListView):
    paginate_by = 3

    def get_queryset(self):
        param_cate = self.request.GET.get('category')
        param_tag = self.request.GET.get('tag')
        if param_cate:
            qs = Post.objects.filter(category__name__iexact=param_cate)
        elif param_tag:
            qs = Post.objects.filter(tags__name__iexact=param_tag)
        else:
            qs = Post.objects.all()
        return qs

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
    model = Post

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        post = obj_to_post(obj)
        prev_post, next_post = prev_next_post(obj)

        qs_comment = obj.comment_set.all()
        comment_list = [obj_to_comment(obj) for obj in qs_comment]

        json_data = {
            'post': post,
            'prevPost': prev_post,
            'nextPost': next_post,
            'commentList': comment_list,
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


class ApiCommentCreateView(BaseCreateView):
    model = Comment
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        comment = obj_to_comment(self.object)
        return JsonResponse(data=comment, safe=True, status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)
