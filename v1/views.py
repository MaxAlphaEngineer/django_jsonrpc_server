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

from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, Result, Success, dispatch

from v1.modules import authorization
from v1.utils.decorators import requires_json
from v1.utils.helper import json_response


@method(name="login")
def login(username, password, refresh=False) -> Result:
    response = authorization.login(username=username, password=password, refresh=refresh)
    print(response)
    return Success(response)


@method
def register() -> Result:
    return Success("pong")


@csrf_exempt
@requires_json
def jsonrpc(request):
    print(request)
    response = dispatch(request.data)

    return json_response(response)
