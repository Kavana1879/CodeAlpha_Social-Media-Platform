from django.contrib import admin
from .models import UserProfile, Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'glow_color', 'description')
    list_filter = ('glow_color',)
    search_fields = ('name', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'joined_date')
    list_filter = ('branch', 'joined_date')
    search_fields = ('user__username', 'branch', 'skills')
    filter_horizontal = ('badges', 'followers')
