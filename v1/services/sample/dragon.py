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
from json import JSONDecodeError

import requests
import xmltodict

from v1.utils.helper import error_message


def fire(payload):
    url = "https://cbu.uz/en/arkhiv-kursov-valyut/json/"  # Replace with your API endpoint URL

    try:
        # send request
        response = requests.post(url, data=payload)
    except requests.exceptions as e:  # timeout, read timeout or ...  ?

        print(e)
        return error_message(-32104)

    try:
        # Process the response
        response = response.json()
    except JSONDecodeError as e:  # not valid json returned
        print(e)
        return error_message(-32701)

    # Return response
    return response


def ws_fire(payload):
    url = 'https://cbu.uz/en/arkhiv-kursov-valyut/xml/'

    # send request
    try:
        response = requests.post(url, data=payload)
    except requests.exceptions as e:  # timeout, read timeout or ...  ?

        print(e)
        return error_message(-32104)

    try:
        # xml to dict parse
        response = xmltodict.parse(response.content)
    except Exception as e:  # parse error occurred
        print(e)

    return response  # Return response
