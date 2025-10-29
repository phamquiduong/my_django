from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'display_name', 'email', 'phone_number', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Email', {'fields': ('email', 'email_verified')}),
        ('Phone number', {'fields': ('phone_number', 'phone_number_verified')}),
        ('Personal info', {'fields': ('display_name',)}),
        ('Location', {'fields': ('provide', 'ward')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
