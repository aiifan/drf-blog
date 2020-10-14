from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class UserProfile(AbstractUser):
    nick_name = models.CharField('昵称', max_length=100, null=True, blank=True)
    mobile = models.CharField(null=True, blank=True, max_length=11, unique=True, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True, verbose_name="邮箱")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    # mobile = models.CharField(max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, verbose_name="邮箱")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code