from django.db import models


class Message(models.Model):
    name = models.CharField('姓名', max_length=80)
    email = models.EmailField('邮箱')
    subject = models.CharField('主题', max_length=160, blank=True)
    content = models.TextField('留言内容')
    is_read = models.BooleanField('是否已读', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '留言'
        verbose_name_plural = '留言'

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"

# Create your models here.
