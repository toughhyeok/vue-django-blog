from django.views.generic import DetailView

from api.utils import (
    obj_to_post,
    prev_next_post
)
from blog.models import (
    Post,
    Category,
    Tag,
)

import json


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        obj = context['object']
        post = obj_to_post(obj)
        prev_post, next_post = prev_next_post(obj)

        qs_cate = Category.objects.all()
        qs_tag = Tag.objects.all()

        cate_list = [cate.name for cate in qs_cate]
        tag_list = [tag.name for tag in qs_tag]

        data_dict = {
            'post': post,
            'prevPost': prev_post,
            'nextPost': next_post,
            'cateList': cate_list,
            'tagList': tag_list,
        }

        context['myJson'] = json.dumps(data_dict)

        return context
