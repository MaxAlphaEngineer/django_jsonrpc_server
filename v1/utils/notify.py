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

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from v1.models import TelegramChat

access_token = "6123968159:AAGPvFcuprvih5bA_0kkAdWyNs9I46gwrtk"


@csrf_exempt
def get_updates(request):
    payload = f'https://api.telegram.org/bot{access_token}/getUpdates'
    response = requests.get(payload).json()

    filtered_chat_data = []

    if response['ok']:
        unique_ids = set()

        for chats in response['result']:
            print(chats)
            if 'message' in chats:
                chat_data = chats['message']['chat']
            elif 'my_chat_member' in chats:
                chat_data = chats['my_chat_member']['chat']
            elif 'channel_post' in chats:
                chat_data = chats['channel_post']['chat']
            else:
                continue  # Skip updates without chat data

            chat_id = chat_data['id']
            if chat_id not in unique_ids:
                unique_ids.add(chat_id)
                filtered_chat_data.append(chat_data)

        # Set offset for future updates
        update_id = response['result'][-1]['update_id']
        requests.get(f'https://api.telegram.org/bot{access_token}/getUpdates?offset={update_id}').json()

    for chat_data in filtered_chat_data:
        print(chat_data)
        chat_id = chat_data.get('id')
        existing_chat = TelegramChat.objects.filter(chat_id=chat_id).first()
        if not existing_chat:
            title = chat_data.get('title')
            first_name = chat_data.get('first_name')
            last_name = chat_data.get('last_name')

            if title and first_name and last_name:
                name = title + ' ' + first_name + ' ' + last_name
            elif title and first_name:
                name = title + ' ' + first_name
            elif first_name and last_name:
                name = first_name + ' ' + last_name
            elif title:
                name = title
            elif first_name:
                name = first_name
            else:
                name = 'Unknown'

            TelegramChat.objects.create(
                chat_id=chat_id,
                chat_type=chat_data.get('type'),
                name=name,
                username=chat_data.get('username'),
                everybody_admin=chat_data.get('all_members_are_administrators', False)
            )
            notify(f"Registered successfully: {name}", chat_id)

    return JsonResponse(filtered_chat_data, safe=False)


def notify(msg, chat_id='', parse_mode='html'):
    params = f'/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={msg}'

    return tg_fire(params)


def notify_all(msg):
    ids = TelegramChat.objects.filter(status=True, active=True)
    for id in ids:
        notify(msg, id.chat_id)


def tg_fire(params):
    url = f'https://api.telegram.org/bot{access_token}{params}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-successful status codes
        result = response.json()
    except requests.RequestException as e:
        # Handle the exception, e.g., log the error or return an error message
        print(f'Failed to send notification: {e}')
        result = {'ok': False, 'error': str(e)}
    return result
