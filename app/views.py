from django.views.generic import ListView

from api.utils import obj_to_post
from blog.models import Post

import json


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        post_list = [obj_to_post(obj) for obj in context['object_list']]
        page_cnt = context['paginator'].num_pages
        cur_page = context['page_obj'].number
        data_dict = {
            'postList': post_list,
            'pageCnt': page_cnt,
            'curPage': cur_page,
        }
        context['myJson'] = json.dumps(data_dict)
        return context
