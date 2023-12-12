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

from v1.models import Partner, TechnicalIssuePeriodTemplate
from v1.models.allowed_ips import IP, AllowedIP
from v1.models.errors import Errors

ALLOWED_METHODS = [
    'errors',
    'users',
    'tip_templates',
    'firewall'
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
    admin = 'admin'
    test = 'test'
    password = 'password'
    if not Partner.objects.filter(username=admin).exists():
        Partner.objects.create_superuser(username=admin, password=password, is_active=True)
        print("Superuser created successfully!")
    else:
        print("Superuser already exists!")

    if not Partner.objects.filter(username=test).exists():
        Partner.objects.create_user(username=test, password=password, is_active=True)
        print("Test user created successfully!")
    else:
        print("Test user already exists!")


def errors():
    for error in rpc_errors:
        # if error code exists do nothing
        rpc_error = Errors.objects.filter(code=error['code'])

        if not rpc_error.exists():
            Errors(code=error['code'], origin=error['origin'], uz=error['uz'], ru=error['ru'], en=error['en']).save()
            print(f'Created: {error["code"]}')

    print('\nError codes populated successfully!\n')


def tip_templates():
    for template in tip_temps:
        # if error code exists do nothing
        tip_temp = TechnicalIssuePeriodTemplate.objects.filter(title=template['title'], uz=template['uz'],
                                                               ru=template['ru'])

        if not tip_temp.exists():
            TechnicalIssuePeriodTemplate(title=template['title'], uz=template['uz'],
                                         ru=template['ru'], en=template['en'], tag=template['tag']).save()
            print(f'Created: {template["title"]}')

    print('\nTemplates  populated successfully!\n')


def firewall():
    for ip_address in ip_addresses:
        # if error code exists do nothing
        ip = IP.objects.filter(ip_address=ip_address['ip_address'], ip_range=ip_address['ip_range'])

        if not ip.exists():
            IP(description=ip_address['description'], ip_range=ip_address['ip_range'],
               ip_address=ip_address['ip_address']).save()
            print(f'Created: {ip_address["description"]}')

    for allowed_ip in allowed_ips:
        allowed = AllowedIP.objects.filter(route=allowed_ip['route'])
        if not allowed.exists():

            _all = AllowedIP(route=allowed_ip['route'],
                             ip_check_allowed=allowed_ip['ip_check_allowed'],
                             is_allowed=allowed_ip['is_allowed'],
                             starts_with=allowed_ip['starts_with']
                             )

            _all.save()

            if allowed_ip['ip_check_allowed']:
                _all.ips.set(IP.objects.all())
                _all.save()

    print('\nIP Addresses populated successfully!\n')


tip_temps = [
    {
        "title": "❗️❗️❗️",
        "uz": "Hurmatli hamkasblar, sizlarga  date kuni Toshkent vaqti bo'yicha start_time va end_time oralig'ida amalga oshiriladigan  texnik ishlar haqida ogohlantirmoqchimiz! \nServislar: service_name  ushbu davrda mavjud bo'lmaydi!\nNoqulaylik uchun uzr so'raymiz.",
        "ru": "Уважаемые коллеги, сообщаем Вам о технических работах на шлюзе, которые date с start_time до end_time по ташкентскому времени!\nУслуги: service_name  в этот период будет недоступен!\nПриносим извинения за неудобства.",
        "en": "Dear colleagues, we would like to inform you about the scheduled maintenance on the gateway, which will take place date  from start_time to end_time according to Tashkent time!\nService: service_name  will be unavailable during this period!\nWe apologize for the inconvenience.",
        "tag": "#issue #pc"
    }
]

ip_addresses = [
    {
        "description": "localhost - for test only",
        "ip_address": "127.0.0.1",
        "ip_range": None,
    },

    {
        "description": "local range - for test only",
        "ip_address": None,
        "ip_range": "127.0.0.1/24",
    }
]

allowed_ips = [
    {
        "route": "/",
        "ip_check_allowed": False,
        "is_allowed": True,
        "starts_with": False,

    },
    {
        "route": "/admin",
        "ip_check_allowed": True,
        "is_allowed": True,
        "starts_with": True,

    },

    {
        "route": "/api/v1/jsonrpc",
        "ip_check_allowed": False,
        "is_allowed": True,
        "starts_with": False,

    }
]

rpc_errors = [
    # Validators
    {
        "code": 300,
        "origin": "access",
        "uz": "Ushbu resursga kirish taqiqlangan!",
        "ru": "Доступ к этому ресурсу запрещен!",
        "en": "Access to this resource is denied!"
    },

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
    {
        "code": -32701,
        "origin": "parse",
        "uz": "JsonRPC qiymatlari formati yaroqsiz",
        "ru": "Недопустимый формат значений JsonRPC",
        "en": "JsonRPC values format is not valid"
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

    {
        "code": -32105,
        "origin": "permission",
        "uz": "Ruxsat etilmagan metod so'rovi",
        "ru": "Недопустимый запрос метода",
        "en": "Not allowed method request"
    },

{
        "code": -32106,
        "origin": "authorization",
        "uz": "Header login taqdim etilmagan",
        "ru": "Header login не указан",
        "en": "Header login is not provided"
    },

    {
        "code": -32107,
        "origin": "authorization",
        "uz": "Header sign taqdim etilmagan",
        "ru": "Header sign не указан",
        "en": "Header sign is not provided"
    },

{
        "code": -32108,
        "origin": "authorization",
        "uz": "Header sign orqali avtorizatsiya muvaffiqayatsiz",
        "ru": "Авторизация с использованием Header sign не удалась",
        "en": "Authorization using Header sign is failed"
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
