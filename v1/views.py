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
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, Result, Success, dispatch


@method(name="login")
def login(username, password) -> Result:
    return Success("pong")


@method
def register() -> Result:
    return Success("pong")


@csrf_exempt
def jsonrpc(request):
    # TODO: check request

    # TODO: authorize

    # TODO: check method is allowed

    # TODO: if logging is enabled for method start logging

    # TODO: request count is enabled start counting

    response = dispatch(request.body.decode())

    return HttpResponse(response, content_type="application/json")
