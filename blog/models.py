from django.db import models


class Post(models.Model):
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    user = models.ForeignKey(
        'UserName', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(
        'DESCRIPTION', max_length=100, blank=True,
        help_text='simple one-line text.')
    title = models.CharField('TITLE', max_length=100)
    url = models.URLField('URL', null=True)
    image = models.ImageField(
        'IMAGE', upload_to='blog/%Y/%m/', blank=True, null=True)
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True)
    update_dt = models.DateTimeField('UPDATE DT', auto_now=True)
    like = models.PositiveSmallIntegerField('LIKE', default=0)

    class Meta:
        ordering = ('-create_dt',)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(
        'DESCRIPTION', max_length=100, blank=True,
        help_text='simple one-line text.')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserName(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
