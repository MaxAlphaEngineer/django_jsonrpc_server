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

from django.core.management import BaseCommand

from v1.models import Partner
from v1.models.errors import Error

ALLOWED_METHODS = [
    'errors',
    'users'
]


class Command(BaseCommand):
    help = ' '

    def add_arguments(self, parser):
        parser.add_argument('model_name', nargs='?', default='errors')

    def handle(self, *args, **options):
        model_name = options['model_name']

        if model_name in ALLOWED_METHODS:
            exec(f'{model_name}()')
        else:
            self.stderr.write(self.style.ERROR(f'Not Allowed Method called to populate!'))


def users():
    username = 'admin'
    password = 'password'
    if not Partner.objects.filter(username=username).exists():
        Partner.objects.create_superuser(username=username, password=password)
    print("Superuser created successfully!")

    # username = 'admin'
    # email = 'admin@example.com'
    # password = 'password'
    # if not User.objects.filter(username=username).exists():
    #     User.objects.create_superuser(username, email, password)
    #     self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
    # else:
    #     self.stdout.write(self.style.WARNING('Superuser already exists'))


def errors():
    for error in rpc_errors:
        # if error code exists do nothing
        rpc_error = Error.objects.filter(code=error['code'])

        if not rpc_error.exists():
            Error(code=error['code'], origin=error['origin'], uz=error['uz'], ru=error['ru'], en=error['en']).save()
            print(f'Created: {error["code"]}')

    print('\nError codes populated successfully!\n')


rpc_errors = [
    # Validators
    {
        "code": 500,
        "origin": "service",
        "uz": "Servis vaqtinchalik mavjud emas!",
        "ru": "Сервис временно недоступен!",
        "en": "Service is temporarily unavailable!"
    },

    {
        "code": -32700,
        "origin": "parse",
        "uz": "So\'rov noto\'g\'ri jo\'natilgan",
        "ru": "Тело запроса неверно",
        "en": "Request body incorrect"
    },

    # AUTHORIZATION
    {
        "code": -32101,
        "origin": "authorization",
        "uz": "Foydalanuvchi nomi yoki parol noto\'g\'ri",
        "ru": "Имя пользователя или пароль неверен",
        "en": "Username or password incorrect"
    },
    {
        "code": -32102,
        "origin": "authorization",
        "uz": "Avtorizatsiya qilish uchun  headerda \'token\' dan foydalaning",
        "ru": "Используйте \'token\' в  header.",
        "en": "Use token in your headers with given for you \'token\' to authorize"
    },
    {
        "code": -32103,
        "origin": "authorization",
        "uz": "Avtorizatsiya tokeni muddati tugagan yoki yaroqsiz",
        "ru": "Срок действия токена авторизации истек или недействителен",
        "en": "Authorization token expired or not valid"
    },

    {
        "code": -32104,
        "origin": "connection",
        "uz": "Ulanishda xatolik yuz berdi",
        "ru": "Ошибка тайм-аута при подключения",
        "en": "Connect timeout error occurred"
    },
    # TERMINAL

    {
        "code": -32301,
        "origin": "terminal",
        "uz": "Merchant yoki terminal mavjud!",
        "ru": "Мерчант или терминал существует!",
        "en": "Merchant or terminal exists!"
    },
    {
        "code": -32302,
        "origin": "terminal",
        "uz": "Merchant yoki terminal mavjud emas!",
        "ru": "Мерчант или терминал не существует!",
        "en": "Merchant or terminal not exists!"
    },
    {
        "code": -32303,
        "origin": "terminal",
        "uz": "Merchant va terminal faol emas!",
        "ru": "Мерчант и терминал не активны!",
        "en": "Merchant and terminal inactive!"
    },

    # CHEQUE
    {
        "code": -32401,
        "origin": "cheque",
        "uz": "External ID oldin foydalanilgan!",
        "ru": "External ID уже существует!",
        "en": "External ID already exists!"
    },

    {
        "code": -32402,
        "origin": "cheque",
        "uz": "External ID topilmadi!",
        "ru": "External ID не найден!",
        "en": "External ID not found!"
    },

]