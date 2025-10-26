from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Article, Comment, Tag


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'image')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for Article model"""
    list_display = ['title', 'slug', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'description', 'body', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model"""
    list_display = ['author', 'article', 'created_at', 'body_preview']
    list_filter = ['created_at', 'author']
    search_fields = ['body', 'author__username', 'article__title']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Body Preview'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model"""
    list_display = ['name', 'created_at', 'article_count']
    search_fields = ['name']
    ordering = ['name']

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Article Count'
