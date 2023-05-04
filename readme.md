# Django - JsonRPC Server Template

A brief description of what this project is all about. This could include some background information on the JSON-RPC
protocol, and how it can be used with Django.

# Installation

Provide instructions for how to install and set up your project. This should include any dependencies that are required,
as well as any configuration steps that need to be taken.

1. Clone Project using git

```commandline
git clone https://github.com/MaxAlphaEngineer/django_jsonrpc_server.git
```

2. Activate Virtual Environment

```commandline
venv\Scripts\activate
```

3. Install requirements.txt

```
pip install -r /path/to/requirements.txt
```

5. Make Migrations

```commandline

python manage.py makemigrations
python manage.py migrate

```

6. Migrate Error codes

```
python manage.py makeerrors
``` 

7. Create Super User

```
python manage.py createsuperuser
``` 

8. Test using API call

POST http://127.0.0.1:8000/api/v1/jsonrpc

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "method": "login",
  "params": {
    "username": "Admin",
    "password": "Password"
  }
}
```

9. Admin Dashboard
Open in browser http://127.0.0.1:8000/admin





# Dependencies

List any external dependencies that are required to use your project, including their version numbers. For example:

1. Django 3.2.4
2. jsonrpcserver 5.0.2
   ...

# Configuration

If there are any configuration steps that need to be taken after the project is installed, list them here. For example,
if your project requires a specific database configuration, you can include instructions for how to set that up.

# Usage

Provide instructions for how to use your project, including any available JSON-RPC methods, custom endpoints, or other
features. You can include code snippets, screenshots, or other visual aids to help users understand how to use your
project.

# Contributing

Provide information about how users can contribute to your project, including any guidelines for submitting pull
requests or reporting issues. You can also include information about how you review and merge contributions.

# License

Include information about the license under which your project is released. For example, if you're using the MIT
license, you could include the following:

MIT License

Copyright (c) 2023 Muzaffar Makhkamov

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

[full license text]

# Acknowledgements

If there are any people, organizations, or resources that you'd like to acknowledge for their contributions to this
project, list them here.
