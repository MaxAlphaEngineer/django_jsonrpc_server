from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from v1.models import Services, Errors
from v1.models.service import TechnicalIssuePeriod, TechnicalIssuePeriodForm
from v1.models.users import Partner
from .models import TelegramChat
from .utils.notify import notify


@admin.register(Partner)
class PartnerAdmin(UserAdmin):
    list_display = 'id', 'username', 'identity', 'is_active', 'is_test', 'is_superuser', 'is_staff'
    list_display_links = 'id', 'username'
    list_editable = ['identity', 'is_active']
    fieldsets = (
        ("Partner Credentials",
         {"fields": ("username", "password", "identity", 'chats')}),
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
        # Get start time
        obj.start_timestamp = timezone.now()

        # Get duration in minutes
        duration = obj.duration

        # calculate end_timestamp
        obj.end_timestamp = obj.start_timestamp + timezone.timedelta(minutes=duration)

        # Create TIP
        obj.save()

        # Set Service status to TEMPORARILY
        # TODO: in case of not recent  start_timestamp do further changes
        service = obj.service
        service.status = Services.StatusType.TEMPORARILY.value
        service.save()

        # TODO: Later make more reliable notify method
        msg = f'🚨🚨 {service} 🚨🚨\n' \
              f'🕧 For {duration} minutes\n' \
              f'Start time: <pre>{obj.start_timestamp}</pre>\n' \
              f'End time: <pre>{obj.end_timestamp}</pre>'
        notify(msg=msg, mode='all')


admin.site.register(TechnicalIssuePeriod, TechnicalIssuePeriodAdmin)


@admin.register(Errors)
class ErrorAdminModel(admin.ModelAdmin):
    list_display = [field.name for field in Errors._meta.fields]


class TelegramChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TelegramChat._meta.fields]
    search_fields = ('name', 'username')
    actions = ['get_updates_action']

    change_list_template = 'telegram_get_updates_change_list.html'


admin.site.register(TelegramChat, TelegramChatAdmin)
