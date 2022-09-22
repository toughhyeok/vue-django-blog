import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings.debug")

from django.core.wsgi import get_wsgi_application  # noqa

get_wsgi_application()

from blog.models import (  # noqa
    Category,
    Tag,
    Post
)

from bs4 import BeautifulSoup  # noqa

import requests  # noqa


class Crawler:
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"} # noqa

    def _get_selector(self, key):
        return self.selector[key]

    def _get_title(self, html):
        return html.select_one(self._get_selector("title")).text

    def _get_category_impl(self, html):
        return

    def _get_category(self, html):
        name = self._get_category_impl(html)
        if '/' in name:
            name = name.split('/')[-1]
        qs = Category.objects.filter(name__exact=name)
        if not qs:
            obj = Category(name=name)
            obj.save()
        else:
            obj = qs.first()
        return obj

    def _get_content_impl(self, raw):
        return

    def _get_content(self, html):
        raw = html.select_one(self._get_selector("content"))
        self._get_content_impl(raw)
        content = ''
        for child in raw.children:
            content += str(child)
        return content

    def _get_tags_impl(self, names):
        return

    def _get_tags(self, html):
        names = [t.text for t in html.select(self._get_selector("tags"))]
        self._get_tags_impl(names)
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

    def _save_post(self, html):
        title = self._get_title(html)
        qs = Post.objects.filter(title__exact=title)
        if not qs:
            post = Post(
                category=self._get_category(html),
                description=title,
                title=title,
                content=self._get_content(html),
            )
            post.save()
            [post.tags.add(t) for t in self._get_tags(html)]

    def _get_html(self, url):
        res = requests.get(url, headers=self.header)
        return BeautifulSoup(res.content, "html.parser")

    def _get_link_list():
        return None

    def crawl(self):
        crawl_list = self._get_link_list()
        for url in crawl_list:
            html = self._get_html(url)
            self._save_post(html)


class HotamulCrawler(Crawler):
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

    def _get_content_impl(self, raw):
        [r.decompose() for r in raw.find_all('div')]

    def _get_tags_impl(self, names):
        pass

    def _get_category_impl(self, html):
        return html.select_one(self._get_selector("category")).text

    def __get_page_nums(self):
        html = self._get_html(self.base_url + self.category_url)
        nums = [s.text for s in html.select(self._get_selector("page"))]
        if len(nums) == 3:
            return [1, ]
        return list(range(int(nums[1]), int(nums[-2])))

    def _get_link_list(self):
        nums = self.__get_page_nums()
        links = []
        for n in nums:
            html = self._get_html(
                self.base_url + self.category_url + f"?page={n}")
            anchors = html.select(self._get_selector("link"))
            for a in anchors:
                links.append(self.base_url + a["href"])
        links.reverse()
        return links


class GiruBoyCrawler(Crawler):
    base_url = "https://velog.io"
    category_name = "share-blog"
    category_url = "/@cgw7976?tag={}".format(category_name)
    selector = {
        "link": "#root > div > div > div:nth-child(4) > div > div > div > a",
        "content": "#root > div > div > div > div.atom-one",
        "title": "#root > div > div > div.head-wrapper > h1",
        "tags": "#root > div > div > div.head-wrapper > div:nth-child(3) > a"
    }

    def _get_content_impl(self, raw):
        pass

    def _get_tags_impl(self, names):
        names.remove(self.category_name)

    def _get_category_impl(self, html):
        return self.category_name

    def _get_link_list(self):
        html = self._get_html(self.base_url + self.category_url)
        anchors = html.select(self._get_selector("link"))
        return [self.base_url + a["href"] for a in anchors]


def create_crawlers():
    return [HotamulCrawler(), GiruBoyCrawler()]


if __name__ == '__main__':
    crawlers = create_crawlers()
    for c in crawlers:
        c.crawl()
