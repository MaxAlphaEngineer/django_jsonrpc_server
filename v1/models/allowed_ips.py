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
    route = models.CharField(max_length=100)
    ips = models.ManyToManyField('IP', related_name='allowed_ips', blank=True)
    ip_check_allowed = models.BooleanField(default=False)

    is_allowed = models.BooleanField(default=False)

    starts_with = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.route} "


class IP(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    ip_range = models.CharField(
        help_text="IP range 192.168.202.0 to 192.168.202.255, you can use the CIDR notation 192.168.202.0/24",
        max_length=18, blank=True, null=True)

    # IP range: 10.0.0.0 to 10.0.0.255
    # CIDR notation: 10.0.0.0/24
    #
    # IP range: 172.16.0.0 to 172.16.0.31
    # CIDR notation: 172.16.0.0/27
    #
    # IP range: 192.168.1.0 to 192.168.1.15
    # CIDR notation: 192.168.1.0/28
    # IP range 192.168.202.0 to 192.168.202.255, you can use the CIDR notation 192.168.202.0/24

    def __str__(self):
        return f"{self.description}  {self.ip_address} {self.ip_range}"
