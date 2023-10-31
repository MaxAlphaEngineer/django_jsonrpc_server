"""
Django settings for api project.

├── api/
├── manage.py
├── env/
│   ├── base.py         Common settings
│   ├── local.py        Local  settings
│   ├─ production.py    Production  settings
│   └─── settings.py
└── ...



"""

import os
from pathlib import Path

APP_NAME = "app_name"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# Common settings applicable to both local and production environments
from env.base import *

PROJECT_CONFIG = config

if DEBUG:
    # Local environment settings
    from env.local import *

else:
    # Production environment settings
    from env.production import *

LOGS_DIR = BASE_DIR / 'logs'

if not LOGS_DIR.exists():
    LOGS_DIR.mkdir()
