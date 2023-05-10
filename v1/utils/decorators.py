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
import json
import time

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist

from v1.models import Partner
from v1.utils.helper import error_message


def requires_json(view_func):
    def wrapper(request, *args, **kwargs):
        request.start_time = time.time()

        # Check valid json format
        try:
            payload = json.loads(request.body)
            # Check contenttype of request and method type
            if not request.content_type == 'application/json' or request.method != 'POST':
                return error_message(-32700, rpc=True, json_response=True)

            # Request Encode
            request.data = request.body.decode()
        except ValueError:
            return error_message(-32700, rpc=True, json_response=True)

        request.id = payload['id']

        request.rpc_method = payload['method']

        # Check method is allowed without login or not ?
        if request.rpc_method not in settings.NO_LOGIN_METHODS:
            # TODO: authorize
            # Check if Authorization header is present
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]

                    # Authenticate the user based on the token
                    try:
                        user = Partner.objects.get(access_token__key=token)
                        request.user = user

                    except Partner.DoesNotExist:
                        return error_message(-32103, rpc=True, json_response=True)
            else:
                return error_message(-32102, rpc=True, json_response=True)

        # Check method is allowed for user
        try:
            # Retrieve the user from the request
            user = request.user

            # Check if the user has the permission
            permission = Permission.objects.get(codename=payload['method'])
            print(user.has_perm(permission))
        except (ObjectDoesNotExist, AttributeError):
            return error_message(-32105, rpc=True, json_response=True)

        # TODO: if logging is enabled for method start logging

        # TODO: request count is enabled start counting

        return view_func(request, *args, **kwargs)

    return wrapper
