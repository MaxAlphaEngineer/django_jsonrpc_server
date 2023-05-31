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
import ipaddress

from django.http import HttpResponseForbidden

from v1.models import AllowedIP


class IPRangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = self.get_client_ip(request)
        if not self.is_ip_allowed(user_ip, request.path_info):
            return HttpResponseForbidden("Access denied")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_ip_allowed(self, ip, path):
        allowed_ips = AllowedIP.objects.filter(is_allowed=True)
        for allowed_ip in allowed_ips:
            if self.ip_matches(allowed_ip.ip_address, ip) or self.ip_matches_range(allowed_ip.ip_range, ip):
                print(allowed_ip.route, path)
                if not allowed_ip.starts_with:
                    if self.path_matches(allowed_ip.route, path):
                        return True
                    else:
                        return False
                if path.startswith(allowed_ip.route):
                    return True

        return False

    def ip_matches(self, allowed_ip, user_ip):
        return allowed_ip == user_ip

    def ip_matches_range(self, allowed_range, user_ip):
        if allowed_range:
            return ipaddress.ip_address(user_ip) in ipaddress.ip_network(allowed_range)
        return False

    def path_matches(self, allowed_path, user_path):
        return allowed_path == user_path
