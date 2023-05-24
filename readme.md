# Django - JsonRPC Server Template

---
Django is a popular web framework that provides a wide range of tools and features for building web applications. One of
the key benefits of Django is its support for building APIs, which can be used to power a wide range of web and mobile
applications.

JSON-RPC is a lightweight and efficient protocol for building APIs that use JSON (JavaScript Object Notation) as their
data format. By using JSON-RPC with Django, developers can build powerful and scalable APIs that can be consumed by a
wide range of client applications.

Reasons why using Django with JSON-RPC:

1. Simple and easy-to-use
2. Lightweight and efficient
3. Flexible and extensible
4. Scalable and reliable

---

# Installation

Provide instructions for how to install and set up your project. This should include any dependencies that are required,
as well as any configuration steps that need to be taken.

1. Clone Project using git

```commandline
git clone https://github.com/MaxAlphaEngineer/django_jsonrpc_server.git
```

2. Install requirements.txt

```commandline
pip install -r requirements.txt
```

3. Activate Virtual Environment

```commandline
venv\Scripts\activate
```

4. Make Migrations

```commandline
python manage.py makemigrations v1
python manage.py migrate
```

5. Populate Error codes, Users and Technical Issue Templates

```commandline
python manage.py populate errors
python manage.py populate users
python manage.py populate tip_templates
```

6. Alternatively you can use custom command from 2~7 steps using

```commandline
python manage.py installapp 
```

7. Test using API call

POST http://127.0.0.1:8000/api/v1/jsonrpc

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "method": "login",
  "params": {
    "username": "admin",
    "password": "password"
  }
}
```

8. Admin Dashboard
   Open in browser http://127.0.0.1:8000/admin

---

# Dependencies

List any external dependencies that are required to use in project listed in [requirements.txt](requirements.txt) file

Such as:

      asgiref==3.6.0
      attrs==23.1.0
      Django==4.2.1
      jsonrpcserver==5.0.9
      * * *

---

# Configuration

Log 
Telegram bot 

---

# Usage

Provide instructions for how to use your project, including any available JSON-RPC methods, custom endpoints, or other
features. You can include code snippets, screenshots, or other visual aids to help users understand how to use your
project.

---

# Contributing

Provide information about how users can contribute to your project, including any guidelines for submitting pull
requests or reporting issues. You can also include information about how you review and merge contributions.

---

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

---

# Acknowledgements

If there are any people, organizations, or resources that you'd like to acknowledge for their contributions to this
project, list them here.
