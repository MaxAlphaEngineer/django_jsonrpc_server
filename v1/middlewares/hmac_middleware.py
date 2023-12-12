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
import base64
import hashlib
import hmac

from django.http import JsonResponse

from v1.models import Partner
from v1.utils.helper import error_message


class HmacMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path_info.startswith('/api/'):
            # Extract the HMAC from the request headers
            username = request.headers.get('Header-Login')
            client_hmac = request.headers.get('Header-Sign')

            if not username:
                return JsonResponse(error_message(-32106, rpc=True))

            if not client_hmac:
                return JsonResponse(error_message(-32107, rpc=True))

            # Fetch the user profile (assuming a UserProfile model with a 'secret' field)
            try:
                partner = Partner.objects.get(username=username)
            except Partner.DoesNotExist:
                return JsonResponse(error_message(300, rpc=True))

            secret = partner.secret.encode('utf-8')
            body = request.body

            digest = hmac.new(secret, body, hashlib.sha256)
            signature = digest.digest()

            sign = base64.b64encode(signature)
            expected_hmac = str(sign, 'UTF-8')

            print(expected_hmac)
            print(client_hmac)

            if not hmac.compare_digest(client_hmac, expected_hmac):
                return JsonResponse(error_message(-32108, rpc=True))

        response = self.get_response(request)
        return response
