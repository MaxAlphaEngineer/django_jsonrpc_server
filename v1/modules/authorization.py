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
from django.contrib.auth import authenticate

from v1.models.users import AccessToken


def generate_custom_token(username, password, refresh):
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        token = AccessToken.objects.filter(Partner=user)
        if token.exists():
            if refresh:
                token.first().generate()
            return {
                "access_token": token.first().key
            }
        else:
            token = AccessToken.objects.create(Partner=user)
            token.partner = user
            token.generate()
            token.save()
            return {
                "access_token": token.key
            }

    else:
        raise Exception('Invalid credentials')
