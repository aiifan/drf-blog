from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField('昵称', max_length=20, null=True,blank=True)
    head = models.ImageField('头像', upload_to='user_head/', null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
