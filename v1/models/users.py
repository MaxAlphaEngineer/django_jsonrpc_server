#  Copyright (c) 2023 - Muzaffar Makhkamov
#
#
#  This file is part of  "Django JsonRPC Server Template".
#
#  "Django JsonRPC Server Template" is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  "Django JsonRPC Server Template" is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with "Django JsonRPC Server Template".  If not, see <http://www.gnu.org/licenses/>.
import hashlib
import os
import secrets
import shutil
import time

import pyzipper
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from v1.models import TelegramChat
from v1.utils.helper import make_dirs


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, file_password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        print("here setting password")
        user.set_password(password, file_password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class Partner(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), unique=True, max_length=50)
    secret = models.CharField(max_length=1024, null=True, blank=True)
    is_test = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    identity = models.CharField(max_length=3, default='TT')
    chats = models.ManyToManyField(
        TelegramChat,
        blank=True,
        related_name='users'
    )
    # email = models.EmailField(default='')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "1. Partners"

    objects = CustomUserManager()

    def generate_secret_key(self):
        self.secret = secrets.token_hex(32)  # Generating a 256-bit (32-byte) hex token

    @property
    def path_to_protected_zip(self):
        return make_dirs(['media', 'protected_zip']) / f'{slugify(self.username)}_secret.zip'

    def generate_protected_zip_with_secret_key_and_password(self, new_password, file_password):
        secret_key = self.secret  # Replace with your actual attribute name
        username = self.username

        # Create a temporary directory
        temp_dir = make_dirs(['tmp', slugify(self.username)])

        # Create a text file with the secret key
        secret_file_path = temp_dir / 'secret.txt'
        with open(secret_file_path, 'w') as secret_file:
            secret_file.write(NOTE)
            secret_file.write(f'Credentials: \n')
            secret_file.write(f'\tSecret Key: {secret_key}\n')
            secret_file.write(f'\tUsername: {username}\n')
            secret_file.write(f'\tPassword: {new_password}\n')


        password = file_password
        print(password)
        with pyzipper.AESZipFile(self.path_to_protected_zip,
                                 'w', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zip_file:
            zip_file.setpassword(bytes(password, 'utf-8'))
            zip_file.write(secret_file_path, 'secret.txt')
        shutil.rmtree(temp_dir)

    def set_password(self, raw_password, file_password):
        self.generate_secret_key()
        self.generate_protected_zip_with_secret_key_and_password(raw_password, file_password)
        super().set_password(raw_password)


class AccessToken(models.Model):
    Partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="access_token")
    key = models.CharField(max_length=256)

    def generate(self):
        timestamp = str(time.time()).encode()

        key = f"{self.Partner.username}:{self.Partner.password}:{timestamp.decode()}"

        hash_object = hashlib.sha256(key.encode())

        self.key = hash_object.hexdigest()
        self.save()

        return self.key

    def rpc_result(self):
        return {
            "result": {
                "access_token": self.key,
                "is_test": self.Partner.is_test,
                "is_superuser": self.Partner.is_superuser,
                "is_staff": self.Partner.is_staff,
                "is_active": self.Partner.is_active,
            }
        }

NOTE = f'''
WARNING: Sensitive Information Enclosed

This file, secret.txt, contains sensitive and confidential information critical to the security of the application. Treat the contents with the utmost care and follow these essential guidelines:

1. Restricted Access:
Limit access to this file to only individuals who absolutely require the information for legitimate reasons. Unauthorized access may lead to security breaches.

2. Avoid Exposure:
Never expose the contents of this file in public repositories, code snippets, or any form of shared documentation. Unauthorized disclosure could compromise the security of your application.

3. Encryption is Advised:
Consider encrypting this file, especially if it needs to be stored in version control or shared between systems. Encryption adds an extra layer of protection against unauthorized access.

4. Regular Audits:
Regularly audit and review who has access to this file. Remove access for individuals who no longer require it.

5. Secure Storage:
Store this file in a secure location with restricted permissions. Avoid storing it in directories that are accessible to a broader audience.

6. Password Changes:
In the event of personnel changes or security concerns, update passwords and credentials immediately.

7. Logging Caution:
Avoid unnecessary logging of sensitive information. If logging is necessary, ensure that logs are stored securely and are subject to regular review.

Failure to comply with these precautions may result in serious security vulnerabilities. Exercise extreme caution, and be vigilant in safeguarding this critical information.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
