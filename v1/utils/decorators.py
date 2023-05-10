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

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from v1.models import Partner
from v1.models.service import Services
from v1.utils.helper import error_message

APP_LABEL = 'v1'


def requires_json(view_func):
    def wrapper(request, *args, **kwargs):
        # --------------------------------------------------------------------------------------------------------------
        # Check valid json format
        try:
            payload = json.loads(request.body)
            request.id = payload['id']
            request.rpc_method = payload['method']
            request.params = payload['params']
            # Check contenttype of request and method type
            if not request.content_type == 'application/json' or request.method != 'POST':
                return error_message(-32700, rpc=True, json_response=True)

            # Request Encode
            request.data = request.body.decode()
        except ValueError:
            return error_message(-32700, rpc=True, json_response=True)
        except KeyError:
            return error_message(-32701, rpc=True, json_response=True)

        # --------------------------------------------------------------------------------------------------------------
        # Check method is allowed without login or not ?
        if request.rpc_method not in settings.NO_LOGIN_METHODS:
            # Check if Authorization header is present
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]

                    # Authenticate the user based on the token
                    try:
                        user = Partner.objects.get(access_token__key=token)
                        request.user = user

                        # ----------------------------------------------------------------------------------------------
                        # Get the content type of the desired model associated with the view
                        permission = Permission.objects.filter(codename=request.rpc_method)
                        if not permission.exists():
                            # Create the permission associated with the app
                            content_type = ContentType.objects.filter(app_label=APP_LABEL).first()
                            Permission.objects.create(codename=request.rpc_method, name=request.rpc_method,
                                                      content_type=content_type)

                        # ----------------------------------------------------------------------------------------------
                        # Check if the user has the permission
                        try:
                            permission = f"{APP_LABEL}.{request.rpc_method}"

                            if not request.user.has_perm(permission):
                                # User does not have the permission
                                return error_message(-32105, rpc=True, json_response=True)
                        except (ObjectDoesNotExist, AttributeError):
                            return error_message(-32106, rpc=True, json_response=True)
                    except Partner.DoesNotExist:
                        return error_message(-32103, rpc=True, json_response=True)
            else:
                return error_message(-32102, rpc=True, json_response=True)

        # --------------------------------------------------------------------------------------------------------------
        service = Services.objects.filter(method_name=request.rpc_method)
        if not service.exists():
            Services.objects.create(method_name=request.rpc_method)
        else:
            service = service.first()
            if service.status != 0:
                return error_message(service.status, rpc=True, json_response=True)
        # --------------------------------------------------------------------------------------------------------------
        # TODO: if logging is enabled for method start logging

        # TODO: request count is enabled start counting

        return view_func(request, *args, **kwargs)

    return wrapper
