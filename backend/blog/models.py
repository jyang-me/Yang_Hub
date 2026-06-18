from django.conf import settings
from django.db import models
from django.utils.text import slugify


def unique_slugify(instance, value, slug_field='slug'):
    base_slug = slugify(value) or 'item'
    slug = base_slug
    model = instance.__class__
    counter = 2

    while model.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug


class Category(models.Model):
    name = models.CharField('分类名称', max_length=80, unique=True)
    slug = models.SlugField('URL 标识', max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名称', max_length=50, unique=True)
    slug = models.SlugField('URL 标识', max_length=80, unique=True, blank=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='作者',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='分类',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True, related_name='posts')
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL 标识', max_length=220, unique=True, blank=True)
    excerpt = models.TextField('摘要', blank=True)
    content = models.TextField('正文内容')
    cover_image = models.ImageField('封面图', upload_to='post_covers/', blank=True, null=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField('是否推荐', default=False)
    published_at = models.DateTimeField('发布时间', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Create your models here.
