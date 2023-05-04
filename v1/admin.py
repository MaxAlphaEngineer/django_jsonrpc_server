from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from v1.models.users import Partner


@admin.register(Partner)
class PartnerAdmin(UserAdmin):
    list_display = 'id', 'username', 'identity', 'chat_id', 'is_active', 'is_test', 'is_superuser', 'is_staff'
    list_display_links = 'id', 'username'
    list_editable = ['identity', 'is_active', 'chat_id']
    fieldsets = (
        ("Partner Credentials",
         {"fields": ("username", "password", "identity", 'chat_id')}),
        (_("Permissions"),
         {"fields": ("is_active", "is_test", "is_staff", "is_superuser", "groups", "user_permissions")})
    )
