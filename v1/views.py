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
from django.contrib.auth.models import Permission
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, Result, Success, dispatch, Error

from v1.models import Services
from v1.modules import authorization
from v1.services.sample import methods
from v1.utils.decorators import requires_json
from v1.utils.helper import json_response


@method(name="login")
def login(context, username, password, refresh=False) -> Result:
    response = authorization.login(username=username, password=password, refresh=refresh)
    return response_handler(response)


@method(name='get.services')
def get_services(context) -> Result:
    # Get the list of permission codenames for the user
    user = context.get('user')

    permissions = user.get_all_permissions()

    permissions = list(permissions)
    return Success(permissions)


@method(name='check.service.permission')
def check_service_permission(context, service_name) -> Result:
    # Get the list of permission codenames for the user
    user = context.get('user')

    permission = Permission.objects.filter(codename=service_name).first()
    service = Services.objects.filter(method_name=service_name).first()

    if not permission:
        # Create the permission associated with the app
        return Success("Not found permission")

    if service:
        if service.is_crud:
            keys = ['create', 'update', 'delete', 'view']

            result = {}
            for key in keys:
                keyword = f'{service_name}.{key}'
                state = Permission.objects.filter(codename=keyword).first()

                res_key = f'can_{key}'
                if not state:
                    result[res_key] = False
                else:
                    permission = f"v1.{keyword}"
                    if user.has_perm(permission):
                        result[res_key] = True
                    else:
                        result[res_key] = False

            return Success(result)

    permission = f"v1.{permission.codename}"
    print(permission)
    if not user.has_perm(permission):
        # User does not have the permission
        return Success(False)

    return Success(True)


@method
def register(context) -> Result:
    return Success("registered")


@method
def create() -> Result:
    return Success("Create")


@method
def update() -> Result:
    return Success("Update")


@method
def delete() -> Result:
    return Success("Update")


@method(name="cbu.rates")
def btc_price(context) -> Result:
    response = methods.get_rates()
    return Success(response)


@csrf_exempt
@requires_json
def jsonrpc(request):
    context = {
        'user': request.user
    }

    response = dispatch(request.data, context=context)

    return json_response(response)


def response_handler(response):
    print(response)
    if 'result' in response:
        return Success(response['result'])
    if 'error' in response:
        return Error(response['error'])
    else:

        return Error(response)
