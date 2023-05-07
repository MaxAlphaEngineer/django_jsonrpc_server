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
import ujson as ujson

from v1.utils.helper import error_message


def requires_json(view_func):
    def wrapper(request, *args, **kwargs):
        # Check valid json format
        try:
            ujson.loads(request.body)
            # Check contenttype of request
            if not request.content_type == 'application/json':
                return error_message(-32700, rpc=True, json_response=True)

            request = request.body.decode()
        except ValueError:
            return error_message(-32700, rpc=True, json_response=True)
        return view_func(request, *args, **kwargs)

    return wrapper


def authorize():
    # TODO: authorize

    # TODO: check method is allowed

    # TODO: if logging is enabled for method start logging

    # TODO: request count is enabled start counting
    pass
