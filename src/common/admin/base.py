from django.contrib import admin


class NoAddAdminMixin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class NoDeleteAdminMixin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


class NoChangeAdminMixin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class ReadOnlyAdminMixin(NoAddAdminMixin, NoDeleteAdminMixin, NoChangeAdminMixin):
    pass
