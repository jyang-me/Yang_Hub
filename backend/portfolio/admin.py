from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'description', 'tech_stack')

# Register your models here.
