import urllib.parse

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from v1.models import Services, Errors, AllowedIP
from v1.models.service import TechnicalIssuePeriod, TechnicalIssuePeriodForm, TechnicalIssuePeriodTemplate
from v1.models.users import Partner
from .models import TelegramChat
from .models.allowed_ips import IP
from .utils.decorators import APP_LABEL
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

    def save_model(self, request, obj, form, change):
        # Save the service
        super().save_model(request, obj, form, change)

        # Create a permission for the service
        codename = f"{obj.method_name.lower()}"
        name = f"{obj.method_name}"

        # Get the content type of the desired model associated with the view
        permission = Permission.objects.filter(codename=codename).first()

        # Create the permission associated with the app
        c_t = ContentType.objects.filter(app_label=APP_LABEL).first()
        if not permission:
            Permission.objects.create(codename=codename, name=name,
                                      content_type=c_t)

        # Create permissions based on the is_crud field
        if obj.is_crud:
            codename = obj.method_name.lower()
            permissions = [
                ('create', f"Can create {obj.method_name}"),
                ('view', f"Can view {obj.method_name}"),
                ('update', f"Can update {obj.method_name}"),
                ('delete', f"Can delete {obj.method_name}")
            ]

            for perm in permissions:
                perm_codename = f'{codename}.{perm[0]}'
                permission = Permission.objects.filter(codename=perm_codename, content_type=c_t).first()
                if not permission:
                    Permission.objects.create(codename=perm_codename, name=perm[1], content_type=c_t)


class TechnicalIssuePeriodAdmin(admin.ModelAdmin):
    form = TechnicalIssuePeriodForm
    list_display = ['service', 'duration', 'start_timestamp', 'end_timestamp']
    fields = ['service', 'duration', 'template', 'notify', 'start_timestamp']

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
        if obj.notify:
            if obj.template is not None:

                date = obj.start_timestamp.strftime('%Y-%m-%d')
                start_time = obj.start_timestamp.strftime('%H:%M')
                end_time = obj.end_timestamp.strftime('%H:%M')

                tag = urllib.parse.quote(obj.template.tag)
                msg = f'<b>{obj.template.title}</b>\n' \
                      f'<pre>-------------------------</pre>\n' \
                      f'🇺🇿 {obj.template.uz}\n' \
                      f'<pre>* * *</pre>\n' \
                      f'🇷🇺 {obj.template.ru}\n' \
                      f'<pre>* * *</pre>\n' \
                      f'🇬🇧 {obj.template.en}\n' \
                      f'<pre>-------------------------</pre>' \
                      f'<pre>{tag}</pre>'

                replacements = {
                    'duration': f'<b>{duration}</b>',
                    'service_name': f'<b>{service.method_name}</b>',
                    'date': f'<b>{date}</b>',
                    'start_time': f'<b>{start_time}</b>',
                    'end_time': f'<b>{end_time}</b>',
                }

                for key, value in replacements.items():
                    msg = msg.replace(key, value)
            else:
                # TODO: Later make more reliable notify method
                msg = f'🚨🚨 {service} 🚨🚨\n' \
                      f'🕧 For {duration} minutes\n' \
                      f'Start time: <pre>{obj.start_timestamp}</pre>\n' \
                      f'End time: <pre>{obj.end_timestamp}</pre>'

            notify(msg=msg, mode='all')


admin.site.register(TechnicalIssuePeriod, TechnicalIssuePeriodAdmin)


@admin.register(TechnicalIssuePeriodTemplate)
class TechnicalIssuePeriodTemplateAdminModel(admin.ModelAdmin):
    # Display all related columns in case of TIP
    list_display = [field.name for field in TechnicalIssuePeriodTemplate._meta.fields]


@admin.register(Errors)
class ErrorAdminModel(admin.ModelAdmin):
    # Error messages DB
    list_display = [field.name for field in Errors._meta.fields]


class TelegramChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TelegramChat._meta.fields]
    search_fields = ('name', 'username')
    actions = ['get_updates_action']

    change_list_template = 'telegram_get_updates_change_list.html'


admin.site.register(TelegramChat, TelegramChatAdmin)


@admin.register(AllowedIP)
class AllowedIPAdminModel(admin.ModelAdmin):
    # Error messages DB
    list_display = [field.name for field in AllowedIP._meta.fields]


@admin.register(IP)
class IPAdminModel(admin.ModelAdmin):
    # Error messages DB
    list_display = [field.name for field in IP._meta.fields]
