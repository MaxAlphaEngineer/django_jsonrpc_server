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
import logging
import os
from datetime import datetime

from v1.utils.helper import json_response


class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Request emitted timestamp
        start_time = datetime.now()

        try:
            response = self.get_response(request)
            # Request proceed timestamp
            end_time = datetime.now()

            # Log the API request and response
            logger = logging.getLogger('api')
            logger.setLevel(logging.DEBUG)

            # Create the log directory if it doesn't exist
            log_dir = os.path.join(os.getcwd(), 'logs', datetime.now().strftime('%Y/%m'))
            os.makedirs(log_dir, exist_ok=True)

            # Create the log file handler
            log_file = os.path.join(log_dir, datetime.now().strftime('%d.log'))
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)

            # Define the log format
            log_format = f'---------------| %(asctime)s - %(levelname)s |---------------%(message)s'
            formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
            fh.setFormatter(formatter)
            # Add the file handler to the logger
            logger.addHandler(fh)

            # Fetch
            host = request.get_host() + request.path
            method = request.method
            client = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
            body = request.body
            content = response.content
            duration = (end_time - start_time).total_seconds()

            # Create message
            message = f"\nHost: {host}" \
                      f"\nMethod: {method}" \
                      f"\nClient: {client} " \
                      f"\nRequest: {body}" \
                      f"\nResponse: {content}" \
                      f"\nDuration: {duration} s"

            # Save log info
            logger.info(message)
            # Return response
            return response

        # In case of exception according request content return response
        except Exception as e:
            if request.method == 'POST' and request.content_type == 'application/json':
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -999,
                        "message": "Invalid params",
                        "data": str(e)
                    },
                    "id": None
                }
                return json_response(error_response)


# TODO: Log request and response according service->logging_type
def log_service_call(request, response, service=None, start_time=None):
    pass
