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
import configparser
import os
from pathlib import Path

# Common settings applicable to both local and production environments
from env.base import *

# config.ini call for project wide usage
config = configparser.ConfigParser()
config.read('env/config.ini')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    # Local environment settings
    from env.local import *
else:
    # Production environment settings
    from env.production import *
