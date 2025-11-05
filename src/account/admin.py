from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

from account.models import Province, User, Ward
from common.admin.base import ReadOnlyAdminMixin


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'display_name', 'email', 'phone_number', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Email', {'fields': ('email', 'email_verified')}),
        ('Phone number', {'fields': ('phone_number', 'phone_number_verified')}),
        ('Personal info', {'fields': ('display_name',)}),
        ('Location', {'fields': ('province', 'ward')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Province)
class ProvinceAdmin(ReadOnlyAdminMixin):
    list_display = ('name', 'name_en', 'full_name', 'full_name_en')
    list_display_links = ('name',)
    fieldsets = ((None, {'fields': ('id', 'name', 'name_en', 'full_name', 'full_name_en')}),)


@admin.register(Ward)
class WardAdmin(ReadOnlyAdminMixin):
    list_display = ('name', 'name_en', 'full_name', 'full_name_en', 'province_link')
    list_filter = ('province',)
    list_display_links = ('name',)
    fieldsets = (
        (None, {'fields': ('id', 'name', 'name_en', 'full_name', 'full_name_en', 'province')}),
    )

    @admin.display(description='Province')
    def province_link(self, obj):
        if not obj.province:
            return '-'
        url = reverse('admin:account_province_change', args=[obj.province.id])
        return format_html("<a href='{}'>{}</a>", url, obj.province.name)
