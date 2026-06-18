from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', blank=True)
    github = models.URLField('GitHub 链接', blank=True)
    linkedin = models.URLField('LinkedIn 链接', blank=True)
    website = models.URLField('个人网站', blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

# Create your models here.
