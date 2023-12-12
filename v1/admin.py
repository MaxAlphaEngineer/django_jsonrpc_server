import os
import secrets
import shutil
import urllib.parse
import zipfile

import pyzipper
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from v1.models import Services, Errors, AllowedIP
from v1.models.service import TechnicalIssuePeriod, TechnicalIssuePeriodForm, TechnicalIssuePeriodTemplate
from v1.models.users import Partner
from .forms import PartnerCreationForm
from .models import TelegramChat
from .models.allowed_ips import IP
from .utils.decorators import APP_LABEL
from .utils.notify import notify


@admin.register(Partner)
class PartnerAdmin(UserAdmin):
    actions = ['generate_secret_key', 'download_secret_key', 'download_credentials']
    list_display = 'id', 'username', 'identity', 'is_active', 'is_test', 'is_superuser', 'is_staff'
    list_display_links = 'id', 'username'
    list_editable = ['identity', 'is_active']
    add_form = PartnerCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'file_password'),
        }),
    )
    fieldsets = (
        ("Partner Credentials",
         {"fields": ("username", "password", "secret", "identity", 'chats')}),
        (_("Permissions"),
         {"fields": ("is_active", "is_test", "is_staff", "is_superuser", "groups", "user_permissions")})
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj = Partner.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                file_password=form.cleaned_data['file_password']
            )
        return super().save_model(request, obj, form, True)


    def generate_secret_key(self, request, queryset):
        for user in queryset:
            user.secret = secrets.token_hex(32)  # Generating a 256-bit (32-byte) hex token
            user.save()

        self.message_user(request, f'Secret keys generated for {queryset.count()} users.')

    generate_secret_key.short_description = 'Generate Secret Key for Selected Users'

    def download_credentials(self, request, queryset):
        if queryset.count() == 1:
            user = queryset.first()
            # Serve the protected zip file as a response
            with open(user.path_to_protected_zip, 'rb') as zip_file_protected:
                response = HttpResponse(zip_file_protected.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{slugify(user.username)}_secret.zip"'
                response['Content-Length'] = os.path.getsize(user.path_to_protected_zip)
                return response
        self.message_user(request, 'Please select only one user for this action.')

    def download_secret_key(self, request, queryset):
        if queryset.count() == 1:
            user = queryset.first()
            secret_key = user.secret  # Replace with your actual attribute name
            username = user.username
            password =  user.password # Replace with the actual attribute name for the login password

            # Create a temporary directory
            temp_dir = os.path.join('/tmp', slugify(user.username))
            os.makedirs(temp_dir, exist_ok=True)

            # Create a text file with the secret key
            secret_file_path = os.path.join(temp_dir, 'secret.txt')
            with open(secret_file_path, 'w') as secret_file:
                secret_file.write(f'Secret Key: {secret_key}\n')
                secret_file.write(f'Username: {username}\n')
                secret_file.write(f'Password: {password}\n')

            # Create a password-protected zip file
            password = secrets.token_urlsafe(16)
            zip_file_path_protected = os.path.join('/tmp', f'{slugify(user.username)}_secret.zip')
            with pyzipper.AESZipFile(zip_file_path_protected, 'w', compression=pyzipper.ZIP_DEFLATED,
                                     encryption=pyzipper.WZ_AES) as zip_file:
                zip_file.setpassword(bytes(password, 'utf-8'))
                zip_file.write(secret_file_path, 'secret.txt')

            print(password)
            # Clean up temporary files
            shutil.rmtree(temp_dir)

            # Serve the protected zip file as a response
            with open(zip_file_path_protected, 'rb') as zip_file_protected:
                response = HttpResponse(zip_file_protected.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{slugify(user.username)}_secret.zip"'
                response['Content-Length'] = os.path.getsize(zip_file_path_protected)
                return response

        self.message_user(request, 'Please select only one user for this action.')

    download_secret_key.short_description = 'Download Secret Key as Protected Zip'


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
