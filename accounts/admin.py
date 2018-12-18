from django.contrib import admin
from .models import Profile, User

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'website_url']
    list_display_links = ['user']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'sex']
