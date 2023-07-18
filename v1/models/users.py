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
import time

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from v1.models import TelegramChat


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        print("here setting password")
        user.set_password(password)
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "1. Partners"

    objects = CustomUserManager()
    pass


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
