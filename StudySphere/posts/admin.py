from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'created_at', 'total_likes')
    list_filter = ('category', 'created_at')
    search_fields = ('user__username', 'caption', 'ai_summary')
    filter_horizontal = ('likes',)
