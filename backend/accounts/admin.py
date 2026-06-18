from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('个人资料', {'fields': ('avatar', 'bio', 'github', 'linkedin', 'website')}),
    )

# Register your models here.
