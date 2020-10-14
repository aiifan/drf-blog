from django.contrib import admin
from .models import UserProfile, VerifyCode
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username','email','nick_name')
    list_display_links = list_display

@admin.register(VerifyCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','code')
    list_display_links = list_display