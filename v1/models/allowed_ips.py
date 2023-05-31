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


class AllowedIP(models.Model):
    ip_address = models.CharField(max_length=45)
    ip_range = models.CharField(max_length=18, blank=True, null=True)
    route = models.CharField(max_length=100)
    is_allowed = models.BooleanField(default=False)
    starts_with = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.route} - {self.ip_address}"
