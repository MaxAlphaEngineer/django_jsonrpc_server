from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from v1.models import Services
from v1.models.service import TechnicalIssuePeriod, TechnicalIssuePeriodForm
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


@admin.register(Services)
class ServicesAdminModel(admin.ModelAdmin):
    list_display = [field.name for field in Services._meta.fields]


class TechnicalIssuePeriodAdmin(admin.ModelAdmin):
    form = TechnicalIssuePeriodForm
    list_display = ['service', 'duration', 'start_timestamp', 'end_timestamp']
    fields = ['service', 'duration', 'start_timestamp']

    def save_model(self, request, obj, form, change):
        obj.start_timestamp = timezone.now()

        duration = obj.duration
        obj.end_timestamp = obj.start_timestamp + duration

        obj.save()

        # Set Service status to TEMPORARILY = 1
        service = obj.service
        service.status = 1
        service.save()

        # Schedule task to set Service status back to ACTIVE = 0 after the period ends
        # end_timestamp = obj.end_timestamp
        # now = timezone.now()
        # if end_timestamp > now:
        #     delay = (end_timestamp - now).total_seconds()
        #     set_active_status.delay(service.id, delay)  # Assuming you have an asynchronous task to update the status


admin.site.register(TechnicalIssuePeriod, TechnicalIssuePeriodAdmin)
