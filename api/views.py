from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from api.utils import (
    obj_to_post,
    prev_next_post,
)
from blog.models import Post


class ApiPostListView(BaseListView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        post_list = [obj_to_post(obj, False) for obj in qs]
        return JsonResponse(data=post_list, safe=False, status=200)


class ApiPostDetailView(BaseDetailView):
    model = Post

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
