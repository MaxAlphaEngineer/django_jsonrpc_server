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

from django.db import models


class Errors(models.Model):
    code = models.IntegerField(unique=True)
    origin = models.CharField(max_length=120, default=None)
    en = models.CharField(max_length=255, default=None)
    uz = models.CharField(max_length=255, default=None)
    ru = models.CharField(max_length=255, default=None)

    def __str__(self):
        return f'JsonRpcError {self.code}: {self.en}'

    class Meta:
        verbose_name = 'Error Message'
        verbose_name_plural = '❌ Error Messages'


class CustomException(models.Model):
    error_message = models.CharField(max_length=255)
    stack_trace = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)