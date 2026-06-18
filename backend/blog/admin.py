from django.contrib import admin

from .models import Category, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'published_at')
    list_filter = ('status', 'is_featured', 'category', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'excerpt', 'content')
    filter_horizontal = ('tags',)

# Register your models here.
