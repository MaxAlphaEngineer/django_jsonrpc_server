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

from django.http import HttpResponseForbidden, JsonResponse

from v1.models import AllowedIP
from v1.utils.helper import error_message


class IPRangeMiddleware:
    # Constructor of middleware
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get Client IP address
        user_ip = self.get_client_ip(request)

        # Check whether ip is allowed or not
        if not self.is_ip_allowed(user_ip, request.path_info):
            if request.content_type == 'application/json':
                return JsonResponse(error_message(300, rpc=True))
            return HttpResponseForbidden("Access denied")

        # Everything is ok return response
        response = self.get_response(request)
        return response

    # Parse IP address from reqeust
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    # IP check using model:Allowed IP
    def is_ip_allowed(self, ip, path):
        # Get from table all IP list
        allowed_ips = AllowedIP.objects.all()

        # If any data not inserted return SUCCESS
        if allowed_ips.count() == 0:
            return True

        # Filter to get all allowed IP list
        allowed_ips = allowed_ips.filter(is_allowed=True)

        for allowed_ip in allowed_ips:
            # If starts with is ENABLED
            if allowed_ip.starts_with:
                if not path.startswith(allowed_ip.route):
                    continue
            else:
                if allowed_ip.route != path:
                    continue
            if not allowed_ip.ip_check_allowed:
                return True

            if allowed_ip.is_allowed:
                ip_addresses = allowed_ip.ips.filter(ip_address=ip)
                ip_ranges = allowed_ip.ips.filter(ip_range__isnull=False).exclude(ip_range='')

                if allowed_ip.starts_with and path.startswith(allowed_ip.route):
                    return True

                if ip_addresses.exists() or self.ip_matches_range(ip_ranges, ip):
                    if not allowed_ip.starts_with:
                        if self.path_matches(allowed_ip.route, path):
                            return True
                        else:
                            return False
                    if path.startswith(allowed_ip.route):
                        return True

        return False

    def ip_matches_range(self, ip_ranges, user_ip):
        for ip_range in ip_ranges:
            if ipaddress.ip_address(user_ip) in ipaddress.ip_network(ip_range.ip_range):
                return True
        return False

    def path_matches(self, allowed_path, user_path):
        return allowed_path == user_path
