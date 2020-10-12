from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nickname')
    list_per_page = 10
    ordering = ('id',)
    list_display_links = ('id', 'username', 'nickname')
