from django.db import models
from django.utils.text import slugify


def unique_slugify(instance, value):
    base_slug = slugify(value) or 'project'
    slug = base_slug
    counter = 2

    while instance.__class__.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug


class Project(models.Model):
    title = models.CharField('项目名称', max_length=160)
    slug = models.SlugField('URL 标识', max_length=180, unique=True, blank=True)
    summary = models.CharField('项目简述', max_length=255)
    description = models.TextField('详细介绍', blank=True)
    tech_stack = models.CharField('技术栈', max_length=255, blank=True)
    cover_image = models.ImageField('项目封面图', upload_to='project_covers/', blank=True, null=True)
    demo_url = models.URLField('演示地址', blank=True)
    source_url = models.URLField('源码地址', blank=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    order = models.PositiveIntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Create your models here.
