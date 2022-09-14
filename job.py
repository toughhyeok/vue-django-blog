import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

from django.core.wsgi import get_wsgi_application  # noqa

get_wsgi_application()

from blog.models import (  # noqa
    Category,
    Tag,
    Post
)

from bs4 import BeautifulSoup  # noqa

import requests  # noqa


class Config:
    base_url = "https://hotamul.tistory.com"
    category_url = "/category/project/share-blog"
    selector = {
        "page": "#mArticle > div.area_paging > span > a > span",
        "link": "#mArticle > div > a.link_post",
        "title": "#mArticle > div.area_title > h3",
        "category": "#mArticle > div.area_title > strong > a",
        "tags": "#mArticle > div.area_etc > dl > dd > a",
        "content": "#mArticle > div.area_view > div",
    }


class Crawler:
    def __init__(self, config):
        self.base_url = config.base_url
        self.category_url = config.category_url
        self.selector = config.selector

    def get_selector(self, key):
        return self.selector[key]

    def get_title(self, html):
        return html.select_one(self.get_selector("title")).text

    def get_category(self, html):
        name = html.select_one(self.get_selector("category")).text
        if '/' in name:
            name = name.split('/')[-1]
        qs = Category.objects.filter(name__exact=name)
        if not qs:
            obj = Category(name=name)
            obj.save()
        else:
            obj = qs.first()
        return obj

    def get_content(self, html):
        raw = html.select_one(self.get_selector("content"))
        [r.decompose() for r in raw.find_all('div')]
        content = ''
        for child in raw.children:
            content += str(child)
        return content

    def get_tags(self, html):
        names = [t.text for t in html.select(self.get_selector("tags"))]
        objs = []
        for n in names:
            qs = Tag.objects.filter(name__exact=n)
            if not qs:
                obj = Tag(name=n)
                obj.save()
            else:
                obj = qs.first()
            objs.append(obj)
        return objs

    def save_post(self, html):
        title = self.get_title(html)
        qs = Post.objects.filter(title__exact=title)
        if not qs:
            post = Post(
                category=self.get_category(html),
                description=title,
                title=title,
                content=self.get_content(html),
            )
            post.save()
            [post.tags.add(t) for t in self.get_tags(html)]

    def get_html(self, url):
        res = requests.get(url)
        return BeautifulSoup(res.content, "html.parser")

    def get_page_nums(self):
        html = self.get_html(self.base_url + self.category_url)
        nums = [s.text for s in html.select(self.get_selector("page"))]
        if len(nums) == 3:
            return [1, ]
        return list(range(int(nums[1]), int(nums[-2])))

    def get_link_list(self):
        nums = self.get_page_nums()
        links = []
        for n in nums:
            html = self.get_html(
                self.base_url + self.category_url + f"?page={n}")
            anchors = html.select(self.get_selector("link"))
            for a in anchors:
                links.append(self.base_url + a["href"])
        return links

    def crawl(self):
        crawl_list = self.get_link_list()
        for url in crawl_list:
            html = self.get_html(url)
            self.save_post(html)


if __name__ == '__main__':
    Crawler(Config).crawl()
