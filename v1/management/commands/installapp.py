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
import subprocess

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Command recommended only in initial run Project Processes: Install from requirements, make migrations, migrate, populate error codes and create test superuser '

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs='?', default='v1')

    def handle(self, *args, **options):
        app_name = options['app_name']
        print(app_name)

        # Call pip to install a package
        self.stdout.write(self.style.SUCCESS('\nStarted Installation from requirements.txt\n'))
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

        # app_name = 'v1'
        self.stdout.write(self.style.SUCCESS(f'\nStarted make migrations: {app_name}\n'))
        call_command('makemigrations', app_name)  # , verbosity=2

        # Perform database migrations
        self.stdout.write(self.style.SUCCESS(f'\nStarted migration!\n'))
        call_command('migrate', app_name)  # , verbosity=2

        # Populate error codes
        call_command('populate', 'errors')

        # TODO: Implement create test superuser
        call_command('populate', 'users')

        # Populate TIP Templates
        call_command('populate', 'tip_templates')
