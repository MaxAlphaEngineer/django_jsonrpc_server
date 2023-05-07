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
import datetime

from django.http import JsonResponse

from v1.models import Error


def error_message(code, message=None, origin="", request_id=None, wrapper=False, rpc=False, json_response=False,
                  rpc_error=False):
    error = Error.objects.filter(code=code)
    if error.exists():
        error = error.first()
        message = {
            "uz": error.uz,
            "ru": error.ru,
            "en": error.en
        }
        data = {
            "code": error.code,
            "message": message
        }
    else:
        if message is None:
            message = {
                "uz": "Nomalum xatolik yuz berdi",
                "ru": "Произошла неопределенная ошибка",
                "en": "Undefined error occurred",
            }
            data = {
                "code": code,
                "message": message
            }
        else:
            data = {
                "code": code,
                "message": message
            }

    if wrapper:
        data = {"error": data}

    if rpc:
        data = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": data,
            "status": False,
            "origin": origin,
            "host": {
                "host": "settings.APP_NAME",
                "timestamp": str(datetime.datetime.now())
            }
        }

    if json_response:
        data = JsonResponse(data, safe=False)

    if rpc_error:
        from jsonrpcserver import Error as RpcError
        return RpcError(code, message)

    return data
