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
from datetime import datetime

from django.http import JsonResponse


class Actuator:
    def __init__(self):
        self.up_time = datetime.now()

    def get_health(self, request):
        start_time = datetime.now()
        up_time = (start_time - self.up_time).total_seconds()
        response = {
            'status': 'UP',
            'uptime': f'{up_time}s',
            'db': db_status(start_time),
            'cache': cache_status(start_time),
            'memory': memory_status(start_time),
        }
        return JsonResponse(response)


def db_status(start_time):
    elapsed_time = (datetime.now() - start_time).total_seconds()
    return {
        "status": "OK",
        "elapsed_time": f'{elapsed_time}s',
    }


def cache_status(start_time):
    elapsed_time = (datetime.now() - start_time).total_seconds()
    return {
        "status": "OK",
        "elapsed_time": f'{elapsed_time}s',
    }


def memory_status(start_time):
    elapsed_time = (datetime.now() - start_time).total_seconds()
    return {
        "status": "OK",
        "elapsed_time": f'{elapsed_time}s',
    }
