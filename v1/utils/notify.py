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
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from v1.models import TelegramChat

config = settings.PROJECT_CONFIG

access_token = config.get('Credentials', 'BOT_TOKEN')


@csrf_exempt
def get_updates(request):
    payload = f'https://api.telegram.org/bot{access_token}/getUpdates'
    response = requests.get(payload).json()

    filtered_chat_data = []

    if response['ok']:
        unique_ids = set()

        for chats in response['result']:
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
        if len(response['result']) > 0:
            update_id = response['result'][-1]['update_id']
            requests.get(f'https://api.telegram.org/bot{access_token}/getUpdates?offset={update_id}').json()

    for chat_data in filtered_chat_data:
        chat_id = chat_data.get('id')
        existing_chat = TelegramChat.objects.filter(chat_id=chat_id).first()
        if not existing_chat:
            title = chat_data.get('title', '')
            first_name = chat_data.get('first_name', '')
            last_name = chat_data.get('last_name', '')

            name_parts = [part.strip() for part in [title, first_name, last_name] if part.strip()]
            name = ' '.join(name_parts) if name_parts else 'Unknown'

            TelegramChat.objects.create(
                chat_id=chat_id,
                chat_type=chat_data.get('type'),
                name=name,
                username=chat_data.get('username'),
                everybody_admin=chat_data.get('all_members_are_administrators', False)
            )
            notify(f"Registered successfully: {name}", chat_id)

    return redirect(request.META.get('HTTP_REFERER'))
    # return JsonResponse(filtered_chat_data, safe=False)


def notify(msg, chat_id='', mode='single', parse_mode='html'):
    if mode == 'all':
        ids = TelegramChat.objects.filter(status=True, active=True)
        for id in ids:
            params = f'/sendMessage?chat_id={id.chat_id}&parse_mode={parse_mode}&text={msg}'
            fire(params)
    elif mode == 'single':
        params = f'/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={msg}'
        fire(params)
    pass


# Send notification using telegram
def fire(params):
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
