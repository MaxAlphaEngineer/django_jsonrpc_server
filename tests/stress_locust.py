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
import random

from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 5)
    access_token = None  # Initialize the access token attribute
    route = '/api/v1/jsonrpc'

    @task
    def login_task(self):
        id = random.randint(1, 999999)
        # Perform the login and get the access token
        payload = {
            "jsonrpc": "2.0",
            "id": id,
            "method": "login",
            "params": {
                "username": "test",
                "password": "password",
                "refresh": False
            }
        }
        response = self.client.post(self.route, json=payload)
        if response.status_code == 200:
            self.access_token = response.json().get("result").get("access_token")

    @task
    def register(self):
        # Check if access_token is available from the login task
        if self.access_token:
            id = random.randint(1, 999999)
            # Perform the login and get the access token
            payload = {
                "jsonrpc": "2.0",
                "id": id,
                "method": "register",
                "params": []
            }

            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.client.get(self.route, headers=headers)
            # Process data response as needed
        else:
            print("Login task did not provide access_token, cannot access data.")
